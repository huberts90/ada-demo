from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def read_item() -> Any:
    return {"message": "Hello World"}
