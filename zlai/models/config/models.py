from zlai.models.load import *
from zlai.types.models_config import ModelConfig
from zlai.types.generate_config.image import *
from zlai.types.generate_config.audio import *
from zlai.types.generate_config.completion import *


__all__ = [
    "chat_completion_models",
    "diffusers_models",
    "audio_models",
    "embedding_models",
    "total_models",
]


chat_completion_models = {
    "Qwen2-0.5B-Instruct": ModelConfig(
        model_name="Qwen2-0.5B-Instruct",
        model_path="/home/models/Qwen/Qwen2-0.5B-Instruct",
        model_type="completion",
        generate_method=Qwen2Instruct05BGenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "2GB"},
    ),
    "Qwen2-1.5B-Instruct": ModelConfig(
        model_name="Qwen2-1.5B-Instruct",
        model_path="/home/models/Qwen/Qwen2-1.5B-Instruct",
        model_type="completion",
        generate_method=Qwen2Instruct15BGenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "4GB"},
    ),
    "Qwen2-7B-Instruct": ModelConfig(
        model_name="Qwen2-7B-Instruct",
        model_path="/home/models/Qwen/Qwen2-7B-Instruct",
        model_type="completion",
        generate_method=Qwen2Instruct7BGenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "20GB"},
    ),
    "Qwen2-Audio-7B-Instruct": ModelConfig(
        model_name="Qwen2-Audio-7B-Instruct",
        model_path="/home/models/Qwen/Qwen2-Audio-7B-Instruct",
        model_type="completion",
        generate_method=Qwen2Audio7BInstructGenerateConfig,
        load_method=load_qwen2_audio,
        max_memory={"0": "20GB"},
    ),
    "Qwen2-57B-A14B-Instruct-GPTQ-Int4": ModelConfig(
        model_name="Qwen2-57B-A14B-Instruct-GPTQ-Int4",
        model_path="/home/models/Qwen/Qwen2-57B-A14B-Instruct-GPTQ-Int4",
        model_type="completion",
        generate_method=Qwen2GenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "30GB"},
    ),
    "glm-4-9b-chat": ModelConfig(
        model_name="glm-4-9b-chat",
        model_path="/home/models/THUDM/glm-4-9b-chat",
        model_type="completion",
        generate_method=GLM4Chat9BGenerateConfig,
        load_method=load_glm4,
        max_memory={"0": "30GB"},
    ),
    "glm-4-9b-chat-1m": ModelConfig(
        model_name="glm-4-9b-chat-1m",
        model_path="/home/models/THUDM/glm-4-9b-chat-1m",
        model_type="completion",
        generate_method=GLM4Chat9B1MGenerateConfig,
        load_method=load_glm4,
        max_memory={"0": "30GB"},
    ),
    "glm-4v-9b": ModelConfig(
        model_name="glm-4v-9b",
        model_path="/home/models/THUDM/glm-4v-9b",
        model_type="completion",
        generate_method=GLM4V9BGenerateConfig,
        load_method=load_glm4,
        max_memory={"0": "30GB"},
    ),
    "LongWriter-glm4-9b": ModelConfig(
        model_name="LongWriter-glm4-9b",
        model_path="/home/models/THUDM/LongWriter-glm4-9b",
        model_type="completion",
        generate_method=GLM4LongWriter9B,
        load_method=load_glm4_long_writer_glm4,
        max_memory={"0": "30GB"},
    ),
    "LongWriter-llama3.1-8b": ModelConfig(
        model_name="LongWriter-llama3.1-8b",
        model_path="/home/models/THUDM/LongWriter-llama3.1-8b",
        model_type="completion",
        generate_method=Llama3LongWriter8B,
        load_method=load_glm4_long_writer_llama3,
        max_memory={"0": "30GB"},
    ),
    "MiniCPM-V-2_6": ModelConfig(
        model_name="MiniCPM-V-2_6",
        model_path="/home/models/openbmb/MiniCPM-V-2_6",
        model_type="completion",
        generate_method=MiniCPMV26GenerateConfig,
        load_method=load_mini_cpm,
        max_memory={"0": "30GB"},
    ),
    "DeepSeek-V2-Lite-Chat": ModelConfig(
        model_name="DeepSeek-V2-Lite-Chat",
        model_path="/home/models/deepseek-ai/DeepSeek-V2-Lite-Chat",
        model_type="completion",
        generate_method=DeepSeekV2LiteChatGenerateConfig,
        load_method=load_deepseek_v2,
        max_memory={"0": "30GB"},
    ),
    "DeepSeek-Coder-V2-Lite-Instruct": ModelConfig(
        model_name="DeepSeek-Coder-V2-Lite-Instruct",
        model_path="/home/models/deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
        model_type="completion",
        generate_method=DeepSeekCoderV2LiteInstructChatGenerateConfig,
        load_method=load_deepseek_coder_v2,
        max_memory={"0": "30GB"},
    ),
    "codegeex4-all-9b": ModelConfig(
        model_name="codegeex4-all-9b",
        model_path="/home/models/THUDM/codegeex4-all-9b",
        model_type="completion",
        generate_method=CodeGeex4All9BGenerateConfig,
        load_method=load_codegeex4,
        max_memory={"0": "30GB"},
    ),
}

diffusers_models = {
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
}

audio_models = {
    "CosyVoice-300M-SFT": ModelConfig(
        model_name="CosyVoice-300M-SFT",
        model_path="/home/models/FunAudioLLM/CosyVoice-300M-SFT",
        model_type="diffuser",
        generate_method=CosyVoiceGenerateConfig,
        load_method=load_cosy_voice,
        max_memory={"0": "32GB"},
    ),
}

embedding_models = {
    "bge-m3": ModelConfig(
        model_name="CosyVoice-300M-SFT",
        model_path="/home/models/BAAI/bge-m3",
        model_type="embedding",
        load_method=load_embedding,
        max_memory={"0": "32GB"},
    ),
}

total_models = {
    **chat_completion_models,
    **diffusers_models,
    **audio_models,
    **embedding_models,
}
