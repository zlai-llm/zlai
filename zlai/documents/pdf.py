import os
import requests
from io import BytesIO
from PIL import Image
from typing import List, Union, Optional, Literal
try:
    import fitz
    from fitz import Page
except ImportError:
    raise ImportError("Please install PyMuPDF to use this function.")
from zlai.types.documents import Document

from .read import BaseRead


__all__ = [
    "ReadPDF",
]


class ReadPDF(BaseRead):
    """"""
    page_count: int
    documents: List[Document]

    def __init__(
            self,
            path: Optional[str] = None,
            stream: Optional[Union[BytesIO, bytes]] = None,
            url: Optional[str] = None,
            text: Optional[bool] = True,
            image: Optional[bool] = True,
            dpi: Optional[int] = 150,
            **kwargs
    ):
        self.path = path

        if isinstance(stream, bytes):
            stream = BytesIO(stream)

        if url:
            stream = requests.get(url).content

        self.stream = stream
        self.text = text
        self.image = image
        self.dpi = dpi
        self.pdf = fitz.open(filename=self.path, stream=self.stream)
        self.page_count = self.pdf.page_count
        self.documents = []
        self.kwargs = kwargs
        self._load_pages()

    def __call__(self, *args, **kwargs):
        """"""

    def _load_page_images(self, page: Page) -> List[Image.Image]:
        """"""
        images = []
        if self.image:
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                base_image = self.pdf.extract_image(img[0])
                images.append(Image.open(BytesIO(base_image.get("image"))))
        return images

    def _load_pages(self):
        """"""
        for page_id in range(self.page_count):
            page = self.pdf.load_page(page_id)
            page_content = page.get_text()
            page_images = self._load_page_images(page)
            page_doc = Document(
                page_content=page_content,
                page_images=page_images,
                metadata={
                    "path": self.path,
                    "page_number": page_id,
                    "image_num": len(page_images),
                },
            )
            self.documents.append(page_doc)

    def save_images(self, path: str, prefix_name: Optional[str] = None) -> None:
        """"""
        if prefix_name is None:
            prefix_name = os.path.basename(self.path).split(".")[0]

        for document in self.documents:
            if len(document.page_images) > 0:
                for i, image in enumerate(document.page_images):
                    image_path = os.path.join(path, f"{prefix_name}_page_{document.metadata.get('page_number')}_image_{i}.png")
                    image.save(image_path)

    def save_text(self, path: str, prefix_name: Optional[str] = None) -> None:
        """"""
        if prefix_name is None:
            prefix_name = os.path.basename(self.path).split(".")[0]

        content = "\n\n".join([document.page_content for document in self.documents])
        file_path = os.path.join(path, f"{prefix_name}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def save_structured(self, path: str, prefix_name: Optional[str] = None) -> None:
        """"""
        self.save_text(path=path, prefix_name=prefix_name)
        self.save_images(path=path, prefix_name=prefix_name)

    def trans_page_to_image(self, dpi: Optional[int] = 150) -> List[Image.Image]:
        """"""
        images = []
        for page_number in range(self.page_count):
            page = self.pdf.load_page(page_number)
            pix = page.get_pixmap(dpi=dpi)
            image = Image.frombytes(mode="RGB", size=[pix.width, pix.height], data=pix.samples)
            images.append(image)
        return images
