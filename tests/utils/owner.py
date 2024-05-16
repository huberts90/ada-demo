from sqlmodel import Session

from app.api import crud
from app.core.db.models import Owner
from utils import random_lower_string


def create_random_owner(db: Session) -> Owner:
    name = random_lower_string()
    user = crud.create_owner_if_not_exists(db=db, name=name)
    return user
