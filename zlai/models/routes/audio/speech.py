import os
from fastapi import HTTPException, Response
from zlai.utils import pkg_config
from zlai.models.utils import load_model_config
from zlai.models.tts.generation import LoadModelAudio
from zlai.models import app, logger
from zlai.models.config.models import audio_models
from zlai.types.request.audio import SpeechRequest


__all__ = [
    "audio_speech"
]


@app.post("/audio/speech")
def audio_speech(
    request: SpeechRequest
):
    """"""
    models_config_path = os.path.join(pkg_config.cache_path, "models_config.yml")
    if not os.path.exists(models_config_path):
        resp_content = f"[AudioSpeech] Models config path: {models_config_path} not exists."
        logger.error(resp_content)
        raise HTTPException(status_code=400, detail=resp_content)
    else:
        logger.info(f"[AudioSpeech] Models config path: {models_config_path}")
        models_config = load_model_config(path=models_config_path).get("models_config")
        model_config = models_config.get(request.model)
        base_config = audio_models.get(request.model)

        if model_config is None or base_config is None:
            raise HTTPException(status_code=400, detail="Invalid request, model not exists.")
        else:
            logger.info(f"[AudioSpeech] Model config: {model_config}")
            base_config.update_kwargs(model_path=model_config.get("model_path"))

        generate_config = base_config.generate_method.model_validate(request.gen_kwargs())
        logger.info(f"[ChatCompletion] Generate kwargs: {generate_config.gen_kwargs()}")

        try:
            model = LoadModelAudio(
                model_config=base_config, model_name=request.model,
                generate_config=generate_config, logger=logger,)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Load Model Error: {e}")
        try:
            wav_binary = model.generate()
            response = Response(content=wav_binary, media_type="audio/wav", )
            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Generate Error: {e}")
