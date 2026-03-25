from app.config import config

from pathlib import Path
import os

if Path(__file__).parent == Path(os.getcwd()):
    config.root_dir = "."



from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from data.db import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on start
    init_database()
    yield
    # on close


app = FastAPI(
    title="",
    description="",
    lifespan=lifespan
)

app.mount(
    "/static",
    StaticFiles(directory=config.root_dir / "static"),
    name="static"
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",port=8000, reload=True)