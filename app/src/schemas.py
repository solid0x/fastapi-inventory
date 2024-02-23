from pydantic import BaseModel


class ItemSchema(BaseModel):
    id: int = None
    name: str
