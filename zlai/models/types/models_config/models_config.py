from typing import Any, Type, List, Dict, Union, Callable, Optional, Iterable
from pydantic import BaseModel, Field, ConfigDict
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
from ..generate_config import TypeInferenceGenerateConfig, InferenceGenerateConfig, inference_generate_config_mapping
from ..images_generations import TypeImageGenerateConfig, ImageGenerateConfig, images_generate_config_mapping
from ..embedding import embedding_generate_config_mapping
from ..audio import TypeAudioGenerateConfig, VoiceGenerateConfig, audio_generate_config_mapping


__all__ = [
    "ModelConfig",
    "ToolsConfig",
]


class ToolsConfig(BaseModel):
    """"""
    tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = Field(default='none', description="")
    tools: Optional[Union[Iterable[ChatCompletionToolParam], List[Dict]]] = Field(default=None, description="")


class ModelConfig(BaseModel):
    """"""
    model_config = ConfigDict(protected_namespaces=())
    model_name: Optional[str] = Field(default=None, description="")
    model_path: Optional[str] = Field(default=None, description="")
    model_type: Optional[str] = Field(default=None, description="")
    load_method: Optional[Union[str, Callable]] = Field(default=None, description="")
    max_memory: Optional[Dict[Union[str, int], str]] = Field(default={0: "20GB"}, description="")
    generate_method: Optional[Union[str, Type[TypeAudioGenerateConfig], Type[TypeInferenceGenerateConfig], Type[TypeImageGenerateConfig]]] = Field(
        default=None, description="")

    def __init__(self, **data):
        super().__init__(**data)

        if self.model_type == "completion":
            base_method = InferenceGenerateConfig
            generate_config_mapping = inference_generate_config_mapping
        elif self.model_type == "diffuser":
            base_method = ImageGenerateConfig
            generate_config_mapping = images_generate_config_mapping
        elif self.model_type == "embedding":
            base_method = None
            generate_config_mapping = embedding_generate_config_mapping
        elif self.model_type == "audio":
            base_method = VoiceGenerateConfig
            generate_config_mapping = audio_generate_config_mapping
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

        if isinstance(self.generate_method, str):
            generate_config_method = generate_config_mapping.get(self.generate_method)
            if generate_config_method is not None:
                self.generate_method = generate_config_method

        if self.generate_method is None or isinstance(self.generate_method, str):
            self.generate_method = base_method

    def get(self, key: Any):
        return self.model_dump().get(key)
