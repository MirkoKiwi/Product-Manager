from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.template import Jinja2Templates



router = APIRouter()
template = Jinja2Templates(directory=config.root_dir / "templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return template.TemplateResponse(
        request=request, name="home.html",
    )