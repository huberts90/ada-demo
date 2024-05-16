from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.core.db.schemas import RepositorySchema


@patch('app.api.routes.repositories.cache_repository',
       AsyncMock(return_value=RepositorySchema(id=1, name="rome-repo", owner_id=12)))
def test_get_repository(client: TestClient) -> None:
    response = client.get("/repositories/caesar/rome-repo")
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == "rome-repo"
