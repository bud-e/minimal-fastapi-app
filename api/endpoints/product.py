import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query
from sqlmodel import select

from db.sqlite_utils import SessionDep
from models.product import (
    ProductRequest,
    Product,
    ProductUpdate,
)

router = APIRouter()


@router.post("/product", tags=["Product"], status_code=201, response_model=Product)
def create_product(session: SessionDep, product_data: ProductRequest):
    db_product = Product.model_validate(product_data)
    db_product.created_at = db_product.modified_at = datetime.now(timezone.utc)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.get("/product", tags=["Product"], status_code=200, response_model=list[Product])
def get_products(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=50)] = 50
):
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products


@router.get("/product/{id}", tags=["Product"], status_code=200, response_model=Product)
def get_product_details(session: SessionDep, id: str):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product (id={id}) not found")
    return product


@router.put("/product/{id}", tags=["Product"], status_code=200, response_model=Product)
def update_product(session: SessionDep, id: str, product_data: ProductUpdate):
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail=f"Product (id={id}) not found")
    product_data = product_data.model_dump(exclude_unset=True)
    product_data.update(
        {
            "modified_at": datetime.now(timezone.utc),
        }
    )
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.delete("/product/{id}", tags=["Product"], status_code=204)
def delete_product(session: SessionDep, id: str):
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail=f"Product (id={id}) not found")
    session.delete(db_product)
    session.commit()
    return
