from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.db.database import Base


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    repositories = relationship("Repository", back_populates="owner")


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    payload = Column(JSON, index=False)
    created_at = Column(DateTime, index=False, default=func.now())
    updated_at = Column(DateTime, index=False, default=func.now(), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("owners.id"))

    owner = relationship("Owner", back_populates="repositories")
