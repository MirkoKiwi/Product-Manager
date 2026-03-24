from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse



@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    pass