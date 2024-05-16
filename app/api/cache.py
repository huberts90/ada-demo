import datetime

import httpx
from fastapi import HTTPException
from app.api import crud
from sqlalchemy.orm import Session
from app.core.db.schemas import RepositorySchema
from app.config import PLATFORM_URL, CACHE_EXPIRATION


async def cache_repository(owner_name: str, repository_name: str, db: Session) -> RepositorySchema:
    owner = crud.create_owner_if_not_exists(db, owner_name)
    cached_repository = crud.get_repository(db=db, owner_id=owner.id, repository_name=repository_name)
    if cached_repository:
        if cached_repository.created_at > datetime.datetime.utcnow()-datetime.timedelta(hours=CACHE_EXPIRATION):
            return cached_repository
        else:
            crud.delete_repository(db=db, owner_id=owner.id, repository_name=repository_name)

    payload = await _get_repo_details(f"{PLATFORM_URL}/repos/{owner_name}/{repository_name}")
    repository = crud.create_repository(db=db, owner_id=owner.id, repository_name=repository_name, payload=payload)

    return repository


async def _get_repo_details(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(url)
        if response.status_code == 200 and 'id' in response.json():
            return response.text
        elif response.status_code == 404:
            raise HTTPException(
                status_code=404, detail="Repository does not exist"
            )
        elif response.status_code == 403:
            raise HTTPException(
                status_code=403, detail="Forbidden"
            )
        elif 'id' not in response.json():
            raise HTTPException(
                status_code=502, detail="Invalid response"
            )
        else:
            raise HTTPException(
                status_code=500, detail="Internal error"
            )
