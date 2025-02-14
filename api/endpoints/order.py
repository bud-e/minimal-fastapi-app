from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query
from sqlmodel import select

from db.sqlite_utils import SessionDep
from models.product import Product
from models.order import (
    Order,
    OrderIDResponse,
    OrderStatusRequest,
    OrderLine,
    OrderLineRequest,
    OrderWithOrderLines,
)

router = APIRouter()


@router.post("/order", tags=["Order"], status_code=201, response_model=OrderIDResponse)
def create_order(session: SessionDep, order_lines: list[OrderLineRequest]):
    current_datetime = datetime.now(timezone.utc)
    db_order = Order(
        created_at=current_datetime, modified_at=current_datetime, status="PENDING"
    )
    order_price = 0.0

    no_qty_product_lst = []
    db_products = []
    for order_line in order_lines:
        line_data = order_line.model_dump(exclude_unset=True)

        db_product = session.get(Product, order_line.product_id)

        order_price += db_product.price * order_line.product_qty

        available_qty = db_product.stock
        ordered_qty = order_line.product_qty

        if ordered_qty > available_qty:
            no_qty_product_lst.append(order_line.product_id)
        else:
            db_product.stock -= ordered_qty
            db_product.modified_at = current_datetime
            db_products.append(db_product)

        line_data.update(
            {
                "modified_at": current_datetime,
                "created_at": current_datetime,
                "product_price": db_product.price,
                "order": db_order,
            }
        )
        db_order_line = OrderLine(**line_data)
        session.add(db_order_line)

    if no_qty_product_lst:
        raise HTTPException(
            status_code=400,
            detail=f"We're not able to take your order due to quantity shortage for given product(s) - {no_qty_product_lst}",
        )

    session.commit()

    session.refresh(db_order)
    db_order.price = order_price
    session.add(db_order)

    for db_product in db_products:
        session.add(db_product)

    session.commit()
    return db_order


@router.get(
    "/order-lines", tags=["OrderLine"], status_code=200, response_model=list[OrderLine]
)
def get_order_lines(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=50)] = 50
):
    order_lines = session.exec(select(OrderLine).offset(offset).limit(limit)).all()
    return order_lines


@router.get(
    "/order/{id}", tags=["Order"], status_code=200, response_model=OrderWithOrderLines
)
def get_order_details(session: SessionDep, id: str):
    db_order = session.get(Order, id)
    if not db_order:
        raise HTTPException(status_code=404, detail=f"Order (id={id}) not found")
    return db_order


@router.put("/order/{id}", tags=["Order"], status_code=200, response_model=Order)
def update_order_status(session: SessionDep, id: str, order_data: OrderStatusRequest):
    db_order = session.get(Order, id)
    if not db_order:
        raise HTTPException(status_code=404, detail=f"Order (id={id}) not found")
    order_data = order_data.model_dump(exclude_unset=True)
    order_data.update(
        {
            "modified_at": datetime.now(timezone.utc),
        }
    )
    db_order.sqlmodel_update(order_data)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order
