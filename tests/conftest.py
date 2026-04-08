import sys
import os
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, StaticPool

from main import app
from src.data.db import get_session



sqlite_file_name = root_dir / "tests" / "test.db"
sqlite_url       = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}



@pytest.fixture(name="session")
def session_fixture(request):
    """
    Test Database
    """
    if os.path.exists(sqlite_file_name):
        os.remove(sqlite_file_name)

    engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Overrides production session dependency
    """
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()