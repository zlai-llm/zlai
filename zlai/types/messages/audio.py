import librosa
from io import BytesIO
from urllib.request import urlopen
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal, Union, List, Dict
from .image import TextContent
from .base import Message


__all__ = [
    "AudioContent",
    "AudioMessage",
]


conversation = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {"role": "user", "content": [
        {"type": "audio", "audio_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/glass-breaking-151256.mp3"},
        {"type": "text", "text": "What's that sound?"},
    ]},
    {"role": "assistant", "content": "It is the sound of glass shattering."},
    {"role": "user", "content": [
        {"type": "text", "text": "What can you do when you hear that?"},
    ]},
    {"role": "assistant", "content": "Stay alert and cautious, and check if anyone is hurt or if there is any damage to property."},
    {"role": "user", "content": [
        {"type": "audio", "audio_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/1272-128104-0000.flac"},
        {"type": "text", "text": "What does the person say?"},
    ]},
]


class AudioContent(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    type: Literal["audio"] = "audio"
    audio_url: Optional[Union[BytesIO, str]] = None


class AudioMessage(Message):
    """"""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: Literal["user"] = Field(default="user", description="""The role of the author of this message.""")
    content: Optional[Union[str, List[Union[TextContent, AudioContent]]]] = Field(
        default=None, description="""The content of the message.""")

    def __init__(
            self,
            audios_url: Optional[List[str]] = None,
            audios_path: Optional[List[str]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        _content = None
        if isinstance(self.content, str):
            _content = [self._add_content(self.content)]

            if audios_url:
                for url in audios_url:
                    _content.append(self._add_url(url))
            if audios_path:
                for path in audios_path:
                    _content.append(self._add_path(path))

        elif isinstance(self.content, list):
            _content = self.content

        self.content = _content

    def _encode_audio_path(self, audio_path: str) -> BytesIO:
        """"""
        with open(audio_path, "rb") as audio_file:
            data = BytesIO(audio_file.read())
        return data

    def _encode_audio_url(self, audio_url: str) -> BytesIO:
        """"""
        data = BytesIO(urlopen(audio_url).read())
        return data

    def _add_content(self, content: str) -> TextContent:
        """"""
        return TextContent(text=content)

    def _add_url(self, url: str) -> AudioContent:
        """"""
        audio = self._encode_audio_url(audio_url=url)
        return AudioContent(audio_url=audio)

    def _add_path(self, path: str) -> AudioContent:
        """"""
        audio = self._encode_audio_path(audio_path=path)
        return AudioContent(audio_url=audio)

    def to_message(self, _type: Literal["qwen2-audio"] = "qwen2-audio") -> Dict:
        """"""
        pass

    def get_audios(self, sr) -> Union[None, List]:
        """"""
        if isinstance(self.content, str):
            return None
        elif isinstance(self.content, List):
            audios = []
            for item in self.content:
                if item.type == "audio":
                    audio = librosa.load(item.audio_url, sr=sr)
                    audios.append(audio)
            return audios
