from pathlib import Path
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, func
from typing import Optional
from decimal import Decimal

from src.config import config
from src.data.db import SessionDep
from src.models.product import Product, ProductRead



router    = APIRouter()
templates = Jinja2Templates(directory=config.root_dir / "src/templates")



@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html",
    )



@router.get("/products_list", response_class=HTMLResponse)
async def get_products_list_ui(
    request:   Request,
    session:   SessionDep,
    name:      Optional[str] | None = Query(None),
    min_price: Optional[str] | None = Query(None),
    max_price: Optional[str] | None = Query(None)
):
    statement = select(Product)
    min_val = None
    max_val = None


    if name and name.strip():
        statement = statement.where(func.lower(Product.name).contains(name.lower()))


    if max_price is not None and max_price.strip():
        try:
            max_val = Decimal(max_price)

        except ValueError:
            max_price = None

    if min_price and min_price.strip():
        try:
            curr_min = Decimal(min_price)

            if max_val is not None and curr_min > max_val:
                s_min = min_price.strip()

                while s_min and Decimal(s_min) > max_val:
                    s_min = s_min[:-1]

                min_price = s_min
                min_val = Decimal(min_price) if min_price else None
    
            else:
                min_val = curr_min

        except ValueError:
            min_price = None

    if min_val is not None:
        statement = statement.where(Product.price >= min_val)
    
    if max_val is not None:
        statement = statement.where(Product.price <= max_val)

    products = session.exec(statement).all()

    return templates.TemplateResponse(
        request = request,
        name    = "products.html",
        context = {
            "products":   products,
            "query_name": name or "",
            "query_min":  min_price if min_price is not None else "",
            "query_max":  max_price if max_price is not None else ""
        }
    )



@router.get("/signup", response_class=HTMLResponse)
async def signup_ui(request: Request):
    return templates.TemplateResponse(
        request = request,
        name    = "signup.html"
    )



@router.get("/login", response_class=HTMLResponse)
async def login_ui(request: Request):
    return templates.TemplateResponse(
        request = request,
        name    = "login.html"
    )