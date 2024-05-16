import uvicorn
from fastapi import FastAPI
from app.api.main import api_router
from app.config import PORT

app = FastAPI()
app.include_router(api_router)


def start():
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    start()
