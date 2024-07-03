from pydantic import Field
from typing import Optional, Union
from .openai import *

__all__ = [
    "TypeStepFunGenerate",
    # V1
    "Step8KV1GenerateConfig",
    "Step32KV1GenerateConfig",
    "Step1V8KGenerateConfig",
    "Step1V32KGenerateConfig",
    "Step128KV1GenerateConfig",
    "Step256KV1GenerateConfig",
]


class Step8KV1GenerateConfig(OpenAIGenerateConfig):
    """ step-1-8k """
    model: Optional[str] = Field(default="step-1-8k", description="模型名称")


class Step32KV1GenerateConfig(OpenAIGenerateConfig):
    """ step-1-32k """
    model: Optional[str] = Field(default="step-1-32k", description="模型名称")


class Step1V8KGenerateConfig(OpenAIGenerateConfig):
    """ step-1v-8k """
    model: Optional[str] = Field(default="step-1v-8k", description="模型名称")


class Step1V32KGenerateConfig(OpenAIGenerateConfig):
    """ step-1v-32k """
    model: Optional[str] = Field(default="step-1v-32k", description="模型名称")


class Step128KV1GenerateConfig(OpenAIGenerateConfig):
    """ step-1-128k """
    model: Optional[str] = Field(default="step-1-128k", description="模型名称")


class Step256KV1GenerateConfig(OpenAIGenerateConfig):
    """ step-1-8k """
    model: Optional[str] = Field(default="step-1-256k", description="模型名称")


TypeStepFunGenerate = Union[
    Step8KV1GenerateConfig,
    Step32KV1GenerateConfig,
    Step1V8KGenerateConfig,
    Step1V32KGenerateConfig,
    Step128KV1GenerateConfig,
    Step256KV1GenerateConfig,
]
