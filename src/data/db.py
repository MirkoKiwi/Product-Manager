from sqlmodel import create_engine, SQLModel, Session

import os




sqlite_file_name = config.root_dir / "data/products.db"
sqlite_url       = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine       = create_engine(sqlite_url, connect_args=connect_args, echo=True)     # echo=True shows the SQL query in the output



def init_database() -> None:
    does_exist: bool = os.path.isfile(sqlite_file_name)
    pass