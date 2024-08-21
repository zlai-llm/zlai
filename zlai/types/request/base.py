from pydantic import BaseModel


__all__ = [
    "BaseRequest"
]


class BaseRequest(BaseModel):
    """"""

    def gen_kwargs(self):
        """"""
        kwargs = {k: v for k, v in self.model_dump().items() if v is not None}
        return kwargs
