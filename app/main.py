from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

from database import DATABASE
from app.routers import dialogues

load_dotenv()

# инициализация fastapi
app = FastAPI(
    title="Python Chatbot Project API",
    description="REST API для pet-проекта на React",
    version="0.1.0",
)

# создаем базу или берем существующую, запустится при старте
@app("startup")
async def init_db():
    await DATABASE.init_db()

# Настройка CORS для React фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # порт Vite/Create React App
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(dialogues.router, prefix="/api", tags=["dialogues"])


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}

# запуск fastapi
if __name__ == "__main__":
    uvicorn.run("app:app")
