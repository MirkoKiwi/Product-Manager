from src.config import config

from pathlib import Path
import os

if Path(__file__).parent == Path(os.getcwd()):
    config.root_dir = "."




from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from src.routers import frontend, products
from src.data.db import init_database



@asynccontextmanager
async def lifespan(app: FastAPI):
    # on start
    
    print("\033[36m[DB] \033[0mInit Database")
    init_database()
    print("\033[36m[DB] \033[0mDB Initialized")
    yield
    # on close
    print("\033[36m[main] \033[0mShutting down")




app = FastAPI(
    title="Title Placeholder (main)",
    description="Description Placeholder (main)",
    lifespan=lifespan
)

app.mount(
    "/static",
    StaticFiles(directory=config.root_dir / "src/static"),
    name="static"
)

app.include_router(frontend.router)
app.include_router(products.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",port=8000, reload=True)