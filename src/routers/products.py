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
async def add_product(session: SessionDep, new_product: ProductCreate) -> ProductRead:
    """
    """
    try:
        # Search if the product's name and price are already existing in DBs
        statement = select(Product).where(
            Product.name  == new_product.name,
            Product.price == new_product.price 
        )
        existing_product = session.exec(statement).first()

        if existing_product:
            existing_product.quantity += new_product.quantity  

            session.add(existing_product)
            session.commit()
            session.refresh(existing_product)

            return ProductRead.model_validate(existing_product)

        # else add new product
        product = Product.model_validate(new_product)

        session.add(product)
        session.commit()
        session.refresh(product)
        
        return ProductRead.model_validate(product)


    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding product: {e}")
    



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




# DELETE - /products/{name} Products by name
@router.delete("/", response_model="", status_code=201)
async def remove_product(session: SessionDep, name: str):
    pass