from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

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
async def get_products_list_ui(request: Request, session: SessionDep):

    statement = select(Product)
    products = session.exec(statement).all()

    return templates.TemplateResponse(
        request = request,
        name    = "products.html",
        context = {"products": products}
    )