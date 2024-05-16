import pytest
from collections.abc import Generator
from fastapi.testclient import TestClient
from sqlmodel import Session, delete
from app.core.db.database import engine
from app.main import app
from app.core.db.models import Owner, Repository


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        statement = delete(Owner)
        session.execute(statement)
        statement = delete(Repository)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
