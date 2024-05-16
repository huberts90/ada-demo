from datetime import datetime, timedelta
import pytest
from unittest.mock import patch, Mock
from pytest_httpx import HTTPXMock
from app.api.cache import cache_repository
from sqlmodel import Session
from app.core.db.models import Repository, Owner


@pytest.mark.asyncio
@patch('app.api.cache.crud.create_owner_if_not_exists', Mock(return_value=Owner(id=12)))
@patch('app.api.cache.crud.get_repository',
       Mock(return_value=
            Repository(id=123, name="rome-repo", owner_id=12, created_at=datetime.utcnow()))
       )
async def test_cache_repository_valid_cache(db: Session, httpx_mock: HTTPXMock) -> None:
    print(datetime.now())
    repo = await cache_repository(db=db, owner_name='caesar', repository_name='rome-repo')
    assert repo.owner_id == 12


@pytest.mark.asyncio
@patch('app.api.cache.crud.create_owner_if_not_exists', Mock(return_value=Owner(id=12)))
@patch('app.api.cache.crud.get_repository',
       Mock(return_value=
            Repository(id=123, name="rome-repo", owner_id=12, created_at=datetime.utcnow() - timedelta(hours=2))
            )
       )
@patch('app.api.cache.crud.delete_repository', Mock(return_value=None))
@patch('app.api.cache.crud.create_repository',
       Mock(return_value=
            Repository(id=456, name="rome-repo", owner_id=12, payload='lorem ipsum', created_at=datetime.now()))
       )
async def test_cache_repository_invalid_cache(db: Session, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={
        "id": 1296269,
        "name": "Hello-World",
        "full_name": "octocat/Hello-World"
    })
    repo = await cache_repository(db=db, owner_name='caesar', repository_name='rome-repo')
    assert repo.owner_id == 12
    assert repo.payload == 'lorem ipsum'
