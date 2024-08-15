import os
import httpx
import anyio
from typing import Any, Iterator, AsyncIterator
from typing_extensions import deprecated


__all__ = [
    "HttpxBinaryResponseContent"
]


class HttpxBinaryResponseContent:
    response: httpx.Response

    def __init__(self, response: httpx.Response) -> None:
        self.response = response

    @property
    def content(self) -> bytes:
        return self.response.content

    @property
    def text(self) -> str:
        return self.response.text

    @property
    def encoding(self) -> str | None:
        return self.response.encoding

    @property
    def charset_encoding(self) -> str | None:
        return self.response.charset_encoding

    def json(self, **kwargs: Any) -> Any:
        return self.response.json(**kwargs)

    def read(self) -> bytes:
        return self.response.read()

    def iter_bytes(self, chunk_size: int | None = None) -> Iterator[bytes]:
        return self.response.iter_bytes(chunk_size)

    def iter_text(self, chunk_size: int | None = None) -> Iterator[str]:
        return self.response.iter_text(chunk_size)

    def iter_lines(self) -> Iterator[str]:
        return self.response.iter_lines()

    def iter_raw(self, chunk_size: int | None = None) -> Iterator[bytes]:
        return self.response.iter_raw(chunk_size)

    def write_to_file(
        self,
        file: str | os.PathLike[str],
    ) -> None:
        """Write the output to the given file.

        Accepts a filename or any path-like object, e.g. pathlib.Path

        Note: if you want to stream the data to the file instead of writing
        all at once then you should use `.with_streaming_response` when making
        the API request, e.g. `client.with_streaming_response.foo().stream_to_file('my_filename.txt')`
        """
        with open(file, mode="wb") as f:
            for data in self.response.iter_bytes():
                f.write(data)

    @deprecated(
        "Due to a bug, this method doesn't actually stream the response content, "
        "`.with_streaming_response.method()` should be used instead"
    )
    def stream_to_file(
        self,
        file: str | os.PathLike[str],
        *,
        chunk_size: int | None = None,
    ) -> None:
        with open(file, mode="wb") as f:
            for data in self.response.iter_bytes(chunk_size):
                f.write(data)

    def close(self) -> None:
        return self.response.close()

    async def aread(self) -> bytes:
        return await self.response.aread()

    async def aiter_bytes(self, chunk_size: int | None = None) -> AsyncIterator[bytes]:
        return self.response.aiter_bytes(chunk_size)

    async def aiter_text(self, chunk_size: int | None = None) -> AsyncIterator[str]:
        return self.response.aiter_text(chunk_size)

    async def aiter_lines(self) -> AsyncIterator[str]:
        return self.response.aiter_lines()

    async def aiter_raw(self, chunk_size: int | None = None) -> AsyncIterator[bytes]:
        return self.response.aiter_raw(chunk_size)

    @deprecated(
        "Due to a bug, this method doesn't actually stream the response content, "
        "`.with_streaming_response.method()` should be used instead"
    )
    async def astream_to_file(
        self,
        file: str | os.PathLike[str],
        *,
        chunk_size: int | None = None,
    ) -> None:
        path = anyio.Path(file)
        async with await path.open(mode="wb") as f:
            async for data in self.response.aiter_bytes(chunk_size):
                await f.write(data)

    async def aclose(self) -> None:
        return await self.response.aclose()
