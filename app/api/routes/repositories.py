from fastapi import APIRouter, Depends
from app.api.cache import cache_repository
from sqlalchemy.orm import Session
from app.core.db.database import SessionLocal, Base, engine

router = APIRouter()
Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/{owner_name}/{repository_name}")
async def read_user(owner_name: str, repository_name: str, db: Session = Depends(get_db)):
    repository = await cache_repository(owner_name=owner_name, repository_name=repository_name, db=db)

    return repository
