import os
from io import BytesIO
from PIL import Image
from typing import List, Union, Optional, Literal
from pypdf import PdfReader
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
            mode: Literal["text", "image"] = "text",
            dpi: Optional[int] = 150,
            **kwargs
    ):
        self.path = path

        if isinstance(stream, bytes):
            stream = BytesIO(stream)

        self.stream = stream
        self.mode = mode
        self.dpi = dpi
        self.pdf = PdfReader(stream if stream else path, strict=True)
        self.page_count = len(self.pdf.pages)
        self.documents = []
        self.kwargs = kwargs
        if self.mode == "text":
            self._reading_text()
        elif self.mode == "image":
            self._reading_image(dpi=dpi)

    def __call__(self, *args, **kwargs):
        """"""

    def _reading_text(self):
        """"""
        for page_number in range(self.page_count):
            page = self.pdf.pages[page_number]
            page_images = []
            for count, image_object in enumerate(page.images):
                image = Image.open(BytesIO(image_object.data))
                page_images.append(image)
            page_doc = Document(
                page_content=page.extract_text(extraction_mode="layout"),
                page_images=page_images,
                metadata={
                    "path": self.path,
                    "page_number": page_number,
                    "image_num": len(page_images),
                },
            )
            self.documents.append(page_doc)

    def _reading_image(self, dpi: Optional[int] = 150):
        """"""
        images = self.trans_page_to_image(dpi)
        for i, image in enumerate(images):
            doc = Document(images=[image], metadata={"path": self.path, "image_num": 1, "page_number": i})
            self.documents.append(doc)

    def save_images(self, path: str, prefix_name: Optional[str] = None) -> None:
        """"""
        if prefix_name is None:
            prefix_name = os.path.basename(self.path).split(".")[0]

        for document in self.documents:
            if len(document.page_images) > 0:
                for i, image in enumerate(document.page_images):
                    image_path = os.path.join(path, f"{prefix_name}_page_{document.metadata.get('page_number')}_image_{i}.png")
                    image.save(image_path)

    def trans_page_to_image(self, dpi: Optional[int] = 150) -> List[Image.Image]:
        """"""
        try:
            import fitz
        except ImportError:
            raise ImportError("Please install PyMuPDF to use this function.")
        images = []
        doc = fitz.open(filename=self.path, stream=self.stream)
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            pix = page.get_pixmap(dpi=dpi)
            image = Image.frombytes(mode="RGB", size=[pix.width, pix.height], data=pix.samples)
            images.append(image)
        return images
