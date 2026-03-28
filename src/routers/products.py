from fastapi import APIRouter, HTTPException, Request, Path, Query, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import Session, select, delete

from typing import List, Annotated

from src.config import config
from src.models.product import Product, ProductCreate, ProductUpdate, ProductRead
from src.data.db import SessionDep




router    = APIRouter(prefix="/products")
templates = Jinja2Templates(directory=config.root_dir / "src/templates")



# GET - Products
@router.get("/", response_model=List[ProductRead])
async def get_products(session: SessionDep) -> List[ProductRead]:
    """
    """
    try:
        statement = select(Product)
        products: List[Product] = session.exec(statement).all()
        return products

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {e}")


# POST - Products
@router.post("/", response_model=ProductRead, status_code=201)
async def add_product(session: SessionDep, product: ProductCreate) -> ProductRead:
    """
    """
    try: 
        new_product = Product.model_validate(product)

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return ProductRead.model_validate(new_product)

    except Exception as e:
        session.rollback()
        return HTTPException(status_code=500, detail=f"Error adding product: {e}")
    

# DELETE - Products
@router.delete("/", response_model="", status_code=201)
async def remove_all_product(session: SessionDep) -> str:
    """
    """
    try:
        statement = delete(Product)
        session.exec(statement)
        session.commit()

        return "All Products deleted"

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting all products: {e}")


# DELETE - Products
