import base64
import librosa
from io import BytesIO
from urllib.request import urlopen
from pydantic import ConfigDict, Field
from typing import Optional, Literal, Union, List, Dict
from .content import TextContent, AudioContent
from .base import Message


__all__ = [
    "AudioMessage",
]


class AudioMessage(Message):
    """"""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: Literal["user", "assistant"] = Field(default="user", description="""The role of the author of this message.""")
    content: Optional[Union[str, List[Union[TextContent, AudioContent]]]] = Field(
        default=None, description="""The content of the message.""")

    def __init__(
            self,
            audios: Optional[List[Union[BytesIO, bytes]]] = None,
            audios_url: Optional[List[str]] = None,
            audios_path: Optional[List[str]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        _content = []
        if isinstance(self.content, list):
            _content = self.content
        elif isinstance(self.content, str):
            _content.append(self._add_content(self.content))
        if audios:
            for audio in audios:
                _content.append(self._add_audio(audio))
        if audios_url:
            for url in audios_url:
                _content.append(self._add_url(url))
        if audios_path:
            for path in audios_path:
                _content.append(self._add_path(path))
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

    def _add_content(self, content: Optional[str]) -> TextContent:
        """"""
        return TextContent(text=content)

    def _add_audio(self, audio: Union[BytesIO, bytes]) -> AudioContent:
        """"""
        if isinstance(audio, bytes):
            audio = BytesIO(audio)
        return AudioContent(audio_url=audio)

    def _add_url(self, url: str) -> AudioContent:
        """"""
        audio = self._encode_audio_url(audio_url=url)
        return AudioContent(audio_url=audio)

    def _add_path(self, path: str) -> AudioContent:
        """"""
        audio = self._encode_audio_path(audio_path=path)
        return AudioContent(audio_url=audio)

    def to_dict(self, _type: Literal["qwen2-audio"] = "qwen2-audio") -> Dict:
        """"""
        content = ""
        if isinstance(self.content, str):
            content = self.content
        elif isinstance(self.content, list):
            content = []
            for item in self.content:
                if isinstance(item, TextContent):
                    content.append(item.model_dump())
                elif isinstance(item, AudioContent):
                    _item = item.model_dump()
                    _item["audio_url"] = base64.b64encode(item.audio_url.getvalue()).decode('utf-8')
                    content.append(_item)
        return {
            "role": self.role, "content": content
        }

    def to_instance(self):
        """"""
        if isinstance(self.content, list):
            for i, item in enumerate(self.content):
                if isinstance(item, AudioContent) and isinstance(item.audio_url, (bytes, str)):
                    self.content[i].audio_url = BytesIO(base64.b64decode(item.audio_url.encode("utf-8")))
        return self

    def get_audios(self, sr) -> Union[None, List]:
        """"""
        audios = []
        if isinstance(self.content, List):
            for item in self.content:
                if item.type == "audio":
                    audio = librosa.load(item.audio_url, sr=sr)[0]
                    audios.append(audio)
        return audios

    def show_streamlit(self):
        st = self._validate_streamlit()
        if isinstance(self.content, str):
            st.markdown(self.content)
        elif isinstance(self.content, list):
            for _content in self.content:
                if isinstance(_content, TextContent):
                    st.markdown(_content.text)
                if isinstance(_content, AudioContent):
                    audio = _content.audio_url
                    if isinstance(audio, str):
                        audio = BytesIO(base64.b64decode(audio.encode("utf-8")))
                    if isinstance(audio, BytesIO):
                        st.audio(audio, format="audio/wav")
                    else:
                        st.write("Audio can't be displayed.")
