from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import items

# Создаём таблицы при первом запуске
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pet Project API",
    description="REST API для pet-проекта на React",
    version="0.1.0",
)

# Настройка CORS для React фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # порт Vite/Create React App
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(items.router, prefix="/api", tags=["items"])


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}
