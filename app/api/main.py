from fastapi import APIRouter

from app.api.routes import home, repositories


api_router = APIRouter()
api_router.include_router(home.router)
api_router.include_router(repositories.router, prefix="/repositories")
