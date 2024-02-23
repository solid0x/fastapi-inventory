from pydantic import BaseModel


class CreateItemSchema(BaseModel):
    name: str


class ItemSchema(BaseModel):
    id: int
    name: str


class ItemNotFoundSchema(BaseModel):
    detail: str = "Item not found"
