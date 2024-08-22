import time
from logging import Logger
from typing import Any, Dict, Optional, Callable
from zlai.utils.mixin import LoggerMixin
from zlai.types.generate_config.image import *
from zlai.types.models_config import ModelConfig


__all__ = [
    "LoadModelDiffusers",
]


class LoadModelDiffusers(LoggerMixin):
    """"""
    pipe: Any
    model_config: Union[ModelConfig, Dict]
    load_method: Union[Callable, str]

    def __init__(
            self,
            model_path: Optional[str] = None,
            model_config: Optional[ModelConfig] = None,
            model_name: Optional[str] = None,
            generate_config: Optional[ImageGenerateConfig] = None,
            load_method: Optional[str] = "auto",
            logger: Optional[Union[Logger, Callable]] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        self.model_path = model_path
        self.model_config = model_config
        self.model_name = model_name
        self.generate_config = generate_config
        self.logger = logger
        self.verbose = verbose
        self.load_method = load_method
        self.args = args
        self.kwargs = kwargs
        self.set_model_path()
        self.load_model()

    def set_model_path(self):
        """"""
        if self.model_path is not None:
            pass
        else:
            self.model_path = self.model_config.get("model_path")
            self.load_method = self.model_config.get("load_method")

    def load_model(self):
        """"""
        self._logger(msg=f"[{__class__.__name__}] Loading model...", color="blue")
        start_time = time.time()
        self.pipe = self.load_method(self.model_path)
        end_time = time.time()
        self._logger(msg=f"[{__class__.__name__}] Loading Done. Use {end_time - start_time:.2f}s", color="blue")

    def _start_logger(self, prompt: str) -> None:
        """"""
        self._logger(msg=f"[{__class__.__name__}] Generating...", color="green")
        self._logger(msg=f"[{__class__.__name__}] Prompt: {prompt}", color="green")

    def diffusers(self) -> str:
        """"""
        self._start_logger(prompt=self.generate_config.prompt)
        generate_function = self.model_config.inference_method.base
        self._logger(msg=f"[{__class__.__name__}] Generate Function: {generate_function}", color="green")

        if generate_function is None:
            b64_img = f"Not find completion method: {self.model_name}"
        else:
            b64_img = generate_function(self.pipe, generate_config=self.generate_config)

        self._logger(msg=f"[{__class__.__name__}] Generating Done.", color="green")
        return b64_img
