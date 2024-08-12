import time
from logging import Logger
from typing import Any, List, Dict, Union, Optional, Callable

from zlai.utils.mixin import LoggerMixin
from zlai.models.types.images_generations import ImageGenerateConfig
from .load_model import *
from .kolors_diffusers import *


__all__ = [
    "LoadModelDiffusers",
]


class LoadModelDiffusers(LoggerMixin):
    """"""
    pipe: Any
    model_config: Dict
    load_method: str

    def __init__(
            self,
            model_path: Optional[str] = None,
            models_config: Optional[List[Dict]] = None,
            model_name: Optional[str] = None,
            generate_config: Optional[ImageGenerateConfig] = None,
            load_method: Optional[str] = "auto",
            logger: Optional[Union[Logger, Callable]] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        self.model_path = model_path
        self.models_config = models_config
        self.model_name = model_name
        self.generate_config = generate_config
        self.logger = logger
        self.verbose = verbose
        self.load_method = load_method
        self.args = args
        self.kwargs = kwargs
        self.set_model_path()
        self.load_model()
        self.kolors_diffusers_model: List[str] = kolors_diffusers_model

    def set_model_path(self):
        """"""
        if self.model_path is not None:
            pass
        else:
            self.model_config = self.get_model_config(model_name=self.model_name, models_config=self.models_config)
            self.model_path = self.model_config.get("model_path")
            self.load_method = self.model_config.get("load_method")

    def load_model(self):
        """"""
        self._logger(msg=f"[{__class__.__name__}] Loading model...", color="blue")
        start_time = time.time()
        self.pipe = load_method_mapping.get(self.load_method)(self.model_path)
        end_time = time.time()
        self._logger(msg=f"[{__class__.__name__}] Loading Done. Use {end_time - start_time:.2f}s", color="blue")

    def get_model_config(
            self,
            model_name: str,
            models_config: List[Dict],
    ) -> Dict:
        """"""
        for config in models_config:
            if config["model_name"] == model_name:
                return config
        raise ValueError(f"Model {model_name} not found.")

    def _start_logger(self, prompt: str) -> None:
        """"""
        self._logger(msg=f"[{__class__.__name__}] Generating...", color="green")
        self._logger(msg=f"[{__class__.__name__}] Prompt: {prompt}", color="green")

    def diffusers(self) -> str:
        """"""
        self._start_logger(prompt=self.generate_config.prompt)
        if self.model_name in self.kolors_diffusers_model:
            b64_img = kolors_generation(self.pipe, generate_config=self.generate_config)
        else:
            b64_img = f"Not find completion method: {self.model_name}"
        self._logger(msg=f"[{__class__.__name__}] Generating Done.", color="green")
        return b64_img
