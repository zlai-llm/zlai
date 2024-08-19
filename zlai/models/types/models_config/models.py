from .models_config import ModelConfig
from ..generate_config import *
from ..images_generations import *
from ..audio import *
from ...completion import *
from ...diffusers import *
from ...tts import *
from ...embedding import *


__all__ = [
    "models"
]

models = {
    "Qwen2-0.5B-Instruct": ModelConfig(
        model_name="Qwen2-0.5B-Instruct",
        model_path="/home/models/Qwen/Qwen2-0.5B-Instruct",
        model_type="completion",
        generate_method=Qwen205BInstructInferenceGenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "2GB"},
    ),
    "Qwen2-1.5B-Instruct": ModelConfig(
        model_name="Qwen2-1.5B-Instruct",
        model_path="/home/models/Qwen/Qwen2-1.5B-Instruct",
        model_type="completion",
        generate_method=Qwen215BInstructInferenceGenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "4GB"},
    ),
    "Qwen2-7B-Instruct": ModelConfig(
        model_name="Qwen2-7B-Instruct",
        model_path="/home/models/Qwen/Qwen2-7B-Instruct",
        model_type="completion",
        generate_method=Qwen2InstructInferenceGenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "20GB"},
    ),
    "Qwen2-57B-A14B-Instruct-GPTQ-Int4": ModelConfig(
        model_name="Qwen2-57B-A14B-Instruct-GPTQ-Int4",
        model_path="/home/models/Qwen/Qwen2-57B-A14B-Instruct-GPTQ-Int4",
        model_type="completion",
        generate_method=Qwen2InstructInferenceGenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "30GB"},
    ),
    "glm-4-9b-chat": ModelConfig(
        model_name="glm-4-9b-chat",
        model_path="/home/models/THUDM/glm-4-9b-chat",
        model_type="completion",
        generate_method=GLM49BChatInferenceGenerateConfig,
        load_method=load_glm4,
        max_memory={"0": "30GB"},
    ),
    "glm-4-9b-chat-1m": ModelConfig(
        model_name="glm-4-9b-chat-1m",
        model_path="/home/models/THUDM/glm-4-9b-chat-1m",
        model_type="completion",
        generate_method=GLM49BChat1MInferenceGenerateConfig,
        load_method=load_glm4,
        max_memory={"0": "30GB"},
    ),
    "glm-4v-9b": ModelConfig(
        model_name="glm-4v-9b",
        model_path="/home/models/THUDM/glm-4v-9b",
        model_type="completion",
        generate_method=GLM4V9BInferenceGenerateConfig,
        load_method=load_glm4,
        max_memory={"0": "30GB"},
    ),
    "MiniCPM-V-2_6": ModelConfig(
        model_name="MiniCPM-V-2_6",
        model_path="/home/models/openbmb/MiniCPM-V-2_6",
        model_type="completion",
        generate_method=MiniCPMInferenceGenerateConfig,
        load_method=load_mini_cpm,
        max_memory={"0": "30GB"},
    ),
    "Kolors-diffusers": ModelConfig(
        model_name="Kolors-diffusers",
        model_path="/home/models/Kwai-Kolors/Kolors-diffusers",
        model_type="diffuser",
        generate_method=KolorsImageGenerateConfig,
        load_method=load_kolors_diffusers,
        max_memory={"0": "32GB"},
    ),
    "Kolors-image2image": ModelConfig(
        model_name="Kolors-diffusers",
        model_path="/home/models/Kwai-Kolors/Kolors-diffusers",
        model_type="diffuser",
        generate_method=KolorsImage2ImageGenerateConfig,
        load_method=load_kolors_image2image,
        max_memory={"0": "32GB"},
    ),
    "FLUX.1-dev": ModelConfig(
        model_name="FLUX.1-dev",
        model_path="/home/models/black-forest-labs/FLUX.1-dev",
        model_type="diffuser",
        generate_method=FLUXImageGenerateConfig,
        load_method=load_flux_diffusers,
        max_memory={"0": "32GB"},
    ),
    "CosyVoice-300M-SFT": ModelConfig(
        model_name="CosyVoice-300M-SFT",
        model_path="/home/models/FunAudioLLM/CosyVoice-300M-SFT",
        model_type="diffuser",
        generate_method=CosyVoiceGenerateConfig,
        load_method=load_cosy_voice,
        max_memory={"0": "32GB"},
    ),
    "bge-m3": ModelConfig(
        model_name="CosyVoice-300M-SFT",
        model_path="/home/models/BAAI/bge-m3",
        model_type="embedding",
        load_method=load_embedding,
        max_memory={"0": "32GB"},
    ),
}
