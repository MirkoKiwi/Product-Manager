from fastapi import FastAPI

from contextlib import asynccontextmanager
from data.db import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on start
    init_database()
    yield
    # on close


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:src", reload=True)