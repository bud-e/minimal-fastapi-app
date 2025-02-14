from pydantic import validator
from sqlmodel import Field, Relationship, SQLModel

from models.base import (
    BaseModel,
    DateTimeModel,
)


class OrderBase(BaseModel, DateTimeModel, table=False):
    price: float = Field(default=0.0)
    status: str

    @validator("status")
    def validate_status(cls, value):
        if value and value not in ["PENDING", "COMPLETED"]:
            raise ValueError("Invalid value for the Status")
        return value


class Order(OrderBase, table=True):
    order_lines: list["OrderLine"] = Relationship(
        back_populates="order", cascade_delete=True
    )


class OrderIDResponse(BaseModel, table=False):
    pass


class OrderStatusRequest(SQLModel, table=False):
    status: str

    @validator("status")
    def validate_status(cls, value):
        if value and value not in ["PENDING", "COMPLETED"]:
            raise ValueError("Invalid value for the Status")
        return value


class OrderLineRequest(SQLModel, table=False):
    product_id: str
    product_qty: int


class OrderLineBase(BaseModel, DateTimeModel, OrderLineRequest, table=False):
    product_price: float | None = None


class OrderLine(OrderLineBase, table=True):
    order_id: str | None = Field(
        default=None, foreign_key="order.id", ondelete="CASCADE"
    )
    order: Order | None = Relationship(back_populates="order_lines")


class OrderWithOrderLines(OrderBase):
    order_lines: list[OrderLineBase] = []
