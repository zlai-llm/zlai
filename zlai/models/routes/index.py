from ...models import app


__all__ = [
    "home"
]


@app.get("/")
def home():
    """"""
    return {"ZLAI": "This is open source LLM model server."}
