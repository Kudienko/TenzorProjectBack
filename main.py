import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.router import router as weather_router

app = FastAPI()
app.include_router(weather_router)

# Установка библиотек - pip install -r requirements.txt
# Создание миграции - alembic revision --autogenerate -m "Название"
# Применение миграции - alembic upgrade "hash-миграции"

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:53486",
    "http://localhost:3000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:53486",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app)
