from zlai.models.load import *
from zlai.models.completion import *
from zlai.models.diffusers import *
from zlai.models.tts import *
from zlai.models.embedding import *
from zlai.types.models_config import ModelConfig, InferenceMethod
from zlai.types.generate_config.image import *
from zlai.types.generate_config.audio import *
from zlai.types.generate_config.completion import *
from zlai.parse.function_call import *


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
        inference_method=InferenceMethod(
            base=completion_qwen_2,
            stream=stream_completion_qwen_2,
            function_call=parse_qwen2,
        ),
    ),
    "Qwen2-1.5B-Instruct": ModelConfig(
        model_name="Qwen2-1.5B-Instruct",
        model_path="/home/models/Qwen/Qwen2-1.5B-Instruct",
        model_type="completion",
        generate_method=Qwen2Instruct15BGenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "4GB"},
        inference_method=InferenceMethod(
            base=completion_qwen_2,
            stream=stream_completion_qwen_2,
            function_call=parse_qwen2,
        ),
    ),
    "Qwen2-7B-Instruct": ModelConfig(
        model_name="Qwen2-7B-Instruct",
        model_path="/home/models/Qwen/Qwen2-7B-Instruct",
        model_type="completion",
        generate_method=Qwen2Instruct7BGenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "20GB"},
        inference_method=InferenceMethod(
            base=completion_qwen_2,
            stream=stream_completion_qwen_2,
            function_call=parse_qwen2,
        ),
    ),
    "Qwen2-Audio-7B-Instruct": ModelConfig(
        model_name="Qwen2-Audio-7B-Instruct",
        model_path="/home/models/Qwen/Qwen2-Audio-7B-Instruct",
        model_type="completion",
        generate_method=Qwen2Audio7BInstructGenerateConfig,
        load_method=load_qwen2_audio,
        max_memory={"0": "20GB"},
        inference_method=InferenceMethod(
            base=completion_qwen_2_audio,
        ),
    ),
    "Qwen2-57B-A14B-Instruct-GPTQ-Int4": ModelConfig(
        model_name="Qwen2-57B-A14B-Instruct-GPTQ-Int4",
        model_path="/home/models/Qwen/Qwen2-57B-A14B-Instruct-GPTQ-Int4",
        model_type="completion",
        generate_method=Qwen2GenerateConfig,
        load_method=load_qwen2,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen_2,
            stream=stream_completion_qwen_2,
        ),
    ),
    "Qwen2-VL-2B-Instruct": ModelConfig(
        model_name="Qwen2-VL-2B-Instruct",
        model_path="/home/models/Qwen/Qwen2-VL-2B-Instruct",
        model_type="completion",
        generate_method=Qwen2VL2BInstructGenerateConfig,
        load_method=load_qwen2_vl,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen_2_vl,
            stream=stream_completion_qwen_2_vl,
        ),
    ),
    "Qwen2-VL-7B-Instruct": ModelConfig(
        model_name="Qwen2-VL-7B-Instruct",
        model_path="/home/models/Qwen/Qwen2-VL-7B-Instruct",
        model_type="completion",
        generate_method=Qwen2VL7BInstructGenerateConfig,
        load_method=load_qwen2_vl,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen_2_vl,
            stream=stream_completion_qwen_2_vl,
        ),
    ),
    "Qwen2.5-0.5B-Instruct": ModelConfig(
        model_name="Qwen2.5-0.5B-Instruct",
        model_path="/home/models/Qwen/Qwen2.5-0.5B-Instruct",
        model_type="completion",
        generate_method=Qwen25Instruct05BGenerateConfig,
        load_method=load_qwen2_5,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen2_5,
            stream=stream_completion_qwen2_5,
            function_call=parse_qwen2_5,
        ),
    ),
    "Qwen2.5-1.5B-Instruct": ModelConfig(
        model_name="Qwen2.5-1.5B-Instruct",
        model_path="/home/models/Qwen/Qwen2.5-1.5B-Instruct",
        model_type="completion",
        generate_method=Qwen25Instruct15BGenerateConfig,
        load_method=load_qwen2_5,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen2_5,
            stream=stream_completion_qwen2_5,
            function_call=parse_qwen2_5,
        ),
    ),
    "Qwen2.5-3B-Instruct": ModelConfig(
        model_name="Qwen2.5-3B-Instruct",
        model_path="/home/models/Qwen/Qwen2.5-3B-Instruct",
        model_type="completion",
        generate_method=Qwen25Instruct3BGenerateConfig,
        load_method=load_qwen2_5,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen2_5,
            stream=stream_completion_qwen2_5,
            function_call=parse_qwen2_5,
        ),
    ),
    "Qwen2.5-7B-Instruct": ModelConfig(
        model_name="Qwen2.5-7B-Instruct",
        model_path="/home/models/Qwen/Qwen2.5-7B-Instruct",
        model_type="completion",
        generate_method=Qwen25Instruct7BGenerateConfig,
        load_method=load_qwen2_5,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen2_5,
            stream=stream_completion_qwen2_5,
            function_call=parse_qwen2_5,
        ),
    ),
    "Qwen2.5-14B-Instruct": ModelConfig(
        model_name="Qwen2.5-14B-Instruct",
        model_path="/home/models/Qwen/Qwen2.5-14B-Instruct",
        model_type="completion",
        generate_method=Qwen25Instruct14BGenerateConfig,
        load_method=load_qwen2_5,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen2_5,
            stream=stream_completion_qwen2_5,
            function_call=parse_qwen2_5,
        ),
    ),
    "Qwen2.5-32B-Instruct": ModelConfig(
        model_name="Qwen2.5-32B-Instruct",
        model_path="/home/models/Qwen/Qwen2.5-32B-Instruct",
        model_type="completion",
        generate_method=Qwen25Instruct32BGenerateConfig,
        load_method=load_qwen2_5,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen2_5,
            stream=stream_completion_qwen2_5,
            function_call=parse_qwen2_5,
        ),
    ),
    "Qwen2.5-72B-Instruct": ModelConfig(
        model_name="Qwen2.5-72B-Instruct",
        model_path="/home/models/Qwen/Qwen2.5-72B-Instruct",
        model_type="completion",
        generate_method=Qwen25Instruct72BGenerateConfig,
        load_method=load_qwen2_5,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen2_5,
            stream=stream_completion_qwen2_5,
            function_call=parse_qwen2_5,
        ),
    ),
    "Qwen2.5-Coder-1.5B-Instruct": ModelConfig(
        model_name="Qwen2.5-Coder-1.5B-Instruct",
        model_path="/home/models/Qwen/Qwen2.5-Coder-1.5B-Instruct",
        model_type="completion",
        generate_method=Qwen25Coder15BInstructGenerateConfig,
        load_method=load_qwen2_5,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen2_5,
            stream=stream_completion_qwen2_5,
            function_call=parse_qwen2_5,
        ),
    ),
    "Qwen2.5-Coder-7B-Instruct": ModelConfig(
        model_name="Qwen2.5-Coder-7B-Instruct",
        model_path="/home/models/Qwen/Qwen2.5-Coder-7B-Instruct",
        model_type="completion",
        generate_method=Qwen25Coder7BInstructGenerateConfig,
        load_method=load_qwen2_5,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_qwen2_5,
            stream=stream_completion_qwen2_5,
            function_call=parse_qwen2_5,
        ),
    ),
    "glm-4-9b-chat": ModelConfig(
        model_name="glm-4-9b-chat",
        model_path="/home/models/THUDM/glm-4-9b-chat",
        model_type="completion",
        generate_method=GLM4Chat9BGenerateConfig,
        load_method=load_glm4,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_glm_4,
            stream=stream_completion_glm_4,
            function_call=parse_glm4,
        ),
    ),
    "glm-4-9b-chat-1m": ModelConfig(
        model_name="glm-4-9b-chat-1m",
        model_path="/home/models/THUDM/glm-4-9b-chat-1m",
        model_type="completion",
        generate_method=GLM4Chat9B1MGenerateConfig,
        load_method=load_glm4,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_glm_4,
            stream=stream_completion_glm_4,
        ),
    ),
    "glm-4v-9b": ModelConfig(
        model_name="glm-4v-9b",
        model_path="/home/models/THUDM/glm-4v-9b",
        model_type="completion",
        generate_method=GLM4V9BGenerateConfig,
        load_method=load_glm4,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_glm_4,
            stream=stream_completion_glm_4,
        ),
    ),
    "LongWriter-glm4-9b": ModelConfig(
        model_name="LongWriter-glm4-9b",
        model_path="/home/models/THUDM/LongWriter-glm4-9b",
        model_type="completion",
        generate_method=GLM4LongWriter9B,
        load_method=load_glm4_long_writer_glm4,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_long_writer_glm4,
            stream=stream_completion_long_writer_glm4,
        ),
    ),
    "LongWriter-llama3.1-8b": ModelConfig(
        model_name="LongWriter-llama3.1-8b",
        model_path="/home/models/THUDM/LongWriter-llama3.1-8b",
        model_type="completion",
        generate_method=Llama3LongWriter8B,
        load_method=load_glm4_long_writer_llama3,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_long_writer_llama3,
            stream=stream_completion_long_writer_llama3,
        ),
    ),
    "LongCite-glm4-9b": ModelConfig(
        model_name="LongCite-glm4-9b",
        model_path="/home/models/THUDM/LongCite-glm4-9b",
        model_type="completion",
        generate_method=GLM4LongCite9B,
        load_method=load_long_cite_glm4,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_long_cite_glm4,
        ),
    ),
    "LongCite-llama3.1-8b": ModelConfig(
        model_name="LongCite-llama3.1-8b",
        model_path="/home/models/THUDM/LongCite-llama3.1-8b",
        model_type="completion",
        generate_method=Llama3LongCite8B,
        load_method=load_long_cite_llama3,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_long_cite_llama3,
        ),
    ),

    "MiniCPM-V-2_6": ModelConfig(
        model_name="MiniCPM-V-2_6",
        model_path="/home/models/openbmb/MiniCPM-V-2_6",
        model_type="completion",
        generate_method=MiniCPMV26GenerateConfig,
        load_method=load_mini_cpm,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_mini_cpm,
            stream=stream_completion_mini_cpm,
        ),
    ),
    "MiniCPM3-4B": ModelConfig(
        model_name="MiniCPM3-4B",
        model_path="/home/models/openbmb/MiniCPM3-4B",
        model_type="completion",
        generate_method=MiniCPM3GenerateConfig,
        load_method=load_mini_cpm_v_3,
        max_memory={"0": "20GB"},
        inference_method=InferenceMethod(
            base=completion_mini_cpm_v3,
            stream=stream_completion_mini_cpm_v3,
            function_call=parse_mini_cpm_v3,
        ),
    ),
    "DeepSeek-V2-Lite-Chat": ModelConfig(
        model_name="DeepSeek-V2-Lite-Chat",
        model_path="/home/models/deepseek-ai/DeepSeek-V2-Lite-Chat",
        model_type="completion",
        generate_method=DeepSeekV2LiteChatGenerateConfig,
        load_method=load_deepseek_v2,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_deepseek_2,
            stream=stream_completion_deepseek_2,
        ),
    ),
    "DeepSeek-Coder-V2-Lite-Instruct": ModelConfig(
        model_name="DeepSeek-Coder-V2-Lite-Instruct",
        model_path="/home/models/deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
        model_type="completion",
        generate_method=DeepSeekCoderV2LiteInstructChatGenerateConfig,
        load_method=load_deepseek_coder_v2,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_deepseek_coder_v2,
            stream=stream_completion_deepseek_coder_v2,
        ),
    ),
    "codegeex4-all-9b": ModelConfig(
        model_name="codegeex4-all-9b",
        model_path="/home/models/THUDM/codegeex4-all-9b",
        model_type="completion",
        generate_method=CodeGeex4All9BGenerateConfig,
        load_method=load_codegeex4,
        max_memory={"0": "30GB"},
        inference_method=InferenceMethod(
            base=completion_codegeex_4,
            stream=stream_completion_codegeex_4,
        ),
    ),
    "GOT-OCR2_0": ModelConfig(
        model_name="GOT-OCR2_0",
        model_path="/home/models/stepfun-ai/GOT-OCR2_0",
        model_type="completion",
        generate_method=GotOCR2GenerateConfig,
        load_method=load_got_ocr,
        max_memory={"0": "20GB"},
        inference_method=InferenceMethod(
            base=completion_got_ocr,
        ),
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
        inference_method=InferenceMethod(
            base=kolors_generation,
        ),
    ),
    "Kolors-image2image": ModelConfig(
        model_name="Kolors-diffusers",
        model_path="/home/models/Kwai-Kolors/Kolors-diffusers",
        model_type="diffuser",
        generate_method=KolorsImage2ImageGenerateConfig,
        load_method=load_kolors_image2image,
        max_memory={"0": "32GB"},
        inference_method=InferenceMethod(
            base=kolors_img2img_generation,
        ),
    ),
    "FLUX.1-dev": ModelConfig(
        model_name="FLUX.1-dev",
        model_path="/home/models/black-forest-labs/FLUX.1-dev",
        model_type="diffuser",
        generate_method=FLUXImageGenerateConfig,
        load_method=load_flux_diffusers,
        max_memory={"0": "32GB"},
        inference_method=InferenceMethod(
            base=flux_generation,
        ),
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
        inference_method=InferenceMethod(
            base=cosy_voice_generation,
        ),
    ),
}

embedding_models = {
    "bge-m3": ModelConfig(
        model_name="bge-m3",
        model_path="/home/models/BAAI/bge-m3",
        model_type="embedding",
        load_method=load_embedding,
        max_memory={"0": "32GB"},
        inference_method=InferenceMethod(
            base=bge_encode,
        ),
    ),
    "jina-embeddings-v3": ModelConfig(
        model_name="jina-embeddings-v3",
        model_path="/home/models/jinaai/jina-embeddings-v3",
        model_type="embedding",
        load_method=load_jina_embedding_v3,
        max_memory={"0": "32GB"},
        inference_method=InferenceMethod(
            base=jina_encode,
        ),
    ),
}

total_models = {
    **chat_completion_models,
    **diffusers_models,
    **audio_models,
    **embedding_models,
}

# todo: 测试在外部指定目录找不到模型文件的情况，并补充文档
