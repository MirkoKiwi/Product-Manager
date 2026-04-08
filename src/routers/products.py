from fastapi import APIRouter, HTTPException, Request, Path, Query, Form, Response, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import Session, select, delete, col, func

from typing import List, Annotated
from decimal import Decimal

from src.config import config
from src.models.product import Product, ProductCreate, ProductUpdate, ProductRead
from src.data.db import SessionDep
from src.auth_utils import get_current_user
from src.models.user import User





router    = APIRouter(prefix="/products")
templates = Jinja2Templates(directory=config.root_dir / "src/templates")



# GET - Products
@router.get(
        "/",
        status_code    = 200,
        response_model = List[ProductRead]
        )
async def get_products(
    session:   SessionDep,
    name:      str     | None = Query(None, description="Search by name"),
    min_price: Decimal | None = Query(None, ge=0),
    max_price: Decimal | None = Query(None, ge=0)
) -> List[ProductRead]:
    """
    Retrieves a list of products based on the filters
    
    Args:
        \n\n
        session: Database session dependency
        name: partial name filter
        min_price: minimum price filter
        max_price: maximum price filter

    Returns:
        \n\n
        List[ProductRead]: a list of product filtered by the criteria
    """
    try:
        statement = select(Product)

        if name:
            statement = statement.where(func.lower(Product.name).contains(name.lower()))

        if min_price is not None:
            statement = statement.where(Product.price >= min_price)

        if max_price is not None:
            statement = statement.where(Product.price <= max_price)

        products: List[Product] = session.exec(statement).all()
        return products


    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {e}") from e




# POST - Products
@router.post(
        "/", 
        response_model = ProductRead,
        )
async def add_product(
    session:      SessionDep,
    response:     Response,
    new_product:  ProductCreate,
    current_user: User = Depends(get_current_user)
) -> ProductRead:
    """
    Adds a new product to the Database or update quantity if already existing

    Args:
        \n\n
        session: Database session dependency
        new_product: data of the product to be added
        current_user: authenticated user performing the request

    Returns:
        \n\n
        ProductRead: the created product data
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

            response.status_code = 200
            return ProductRead.model_validate(existing_product)

        # else add new product
        product = Product.model_validate(new_product)

        session.add(product)
        session.commit()
        session.refresh(product)
        
        response.status_code = 201
        return ProductRead.model_validate(product)


    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding product: {e}") from e




# PATCH - Update by ID
@router.patch(
        "/{product_id}",
        status_code    = 200,
        response_model = ProductRead
)
async def product_update(
    session:        SessionDep,
    product_update: ProductUpdate,
    product_id:     int,
    current_user:   User = Depends(get_current_user)
) -> ProductRead:
    """
    Updates a product
    
    Args:
        \n\n
        session: Database session dependency
        product_update: the new data to update the existing product with
        product_id: ID of the product to update
        current_user: authenticated user performing the request

    Returns:
        \n\n
        ProductRead: the updated product data
    """
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(
            status_code = 404, 
            detail      = f"Product {product_id} not found")

    try:
        update_data = product_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_product, key, value)

        session.add(db_product)
        session.commit()
        session.refresh(db_product)

        return ProductRead.model_validate(db_product)


    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code = 500, 
            detail      = f"Error updating product: {e}"
        ) from e




# DELETE - Products
@router.delete(
        "/", 
        status_code    = 200,
        response_model = str
        )
async def remove_all_product(
    session:      SessionDep,
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Removes all products stored in the Database (debug)
    
    Args:
        \n\n
        session: Database session dependencys
        current_user: authenticated user

    Returns:
        \n\n
        dict: confirmation message
    """
    try:
        statement = delete(Product)
        session.exec(statement)
        session.commit()

        return {"message": "All Products deleted!"}


    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code = 500, 
            detail      = f"Error deleting all products: {e}"
        ) from e




# DELETE - /products/{product_id} Products by ID
@router.delete(
        "/{product_id}",
        status_code    = 200,
        response_model = ProductRead
        )
async def remove_product(
    session:      SessionDep, 
    product_id:   int,
    current_user: User = Depends(get_current_user)
) -> ProductRead:
    """
    Removes a product by ID

    Args:
        \n\n
        session: Database session dependency
        product_id: ID of the product to delete
        current_user: authenticated user performing the request

    Returns:
        \n\n
        ProductRead: the deleted product data
    """
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    
    try:
        deleted_product = ProductRead.model_validate(product)

        session.delete(product)
        session.commit()

        return deleted_product


    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting product: {e}") from e