from sqlalchemy.orm import Session
from app.core.db.models import Owner, Repository


def get_owner(db: Session, name: str):
    return db.query(Owner).filter(Owner.name == name).first()


def create_owner_if_not_exists(db: Session, name: str):
    db_owner = get_owner(db, name)
    if db_owner:
        return db_owner
    owner = Owner(name=name)
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


def get_repository(db: Session, owner_id: int, repository_name: str):
    return db.query(Repository).filter(Repository.name == repository_name and Owner.id == owner_id).first()


def create_repository(db: Session, owner_id: int, repository_name: str, payload: str):
    db_repository = db.query(Repository).filter(Repository.name == repository_name).first()
    if db_repository:
        return db_repository
    repository = Repository(name=repository_name, owner_id=owner_id, payload=payload)
    db.add(repository)
    db.commit()
    db.refresh(repository)
    return repository


def delete_repository(db: Session, owner_id: int, repository_name: str):
    repository = get_repository(db=db, owner_id=owner_id, repository_name=repository_name)
    db.delete(repository)
    db.commit()
