from sqlmodel import create_engine, SQLModel, Session
import os
from typing import Annotated
from fastapi import Depends

from src.config import config


# DB Models
from src.models.product import Product
from src.models.user import User


sqlite_file_name = config.root_dir / "src/data/products.db"
sqlite_url       = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine       = create_engine(sqlite_url, connect_args=connect_args, echo=True)




def init_database() -> None:
    does_exist: bool = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]