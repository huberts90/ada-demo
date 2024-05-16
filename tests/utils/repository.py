from sqlmodel import Session

from app.api import crud
from app.core.db.models import Repository
from tests.utils.owner import create_random_owner
from utils import random_lower_string


def create_random_repository(db: Session) -> Repository:
    owner = create_random_owner(db)
    owner_id = owner.id
    assert owner_id is not None
    repository_name = random_lower_string()
    return crud.create_repository(db=db, owner_id=owner_id, repository_name=repository_name)
