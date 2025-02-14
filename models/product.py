from sqlmodel import Field, SQLModel

from models.base import (
    BaseModel,
    DateTimeModel,
)


class ProductRequest(SQLModel, table=False):
    name: str = Field(index=True)
    description: str
    price: float = Field(gt=0)
    stock: int | None


class Product(BaseModel, DateTimeModel, ProductRequest, table=True):
    pass


class ProductUpdate(SQLModel, table=False):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
