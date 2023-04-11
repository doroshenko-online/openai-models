import logging
import os

from fastapi import FastAPI
from databases import Database
from sqlalchemy import create_engine

from register import SingletonDatabase
from routers import router
from models import Base, OpenAIModel

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройки базы данных
DATABASE_URL = os.getenv('PSQL')
OPENAI_ORG_ID = os.getenv('ORG_ID')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')


if not all([
    DATABASE_URL,
    OPENAI_TOKEN,
    OPENAI_ORG_ID
]):
    raise Exception('App needs env variables: PSQL, ORG_ID, OPENAI_TOKEN')

# Инициализация FastAPI
app = FastAPI()

# Настройки базы данных
db_singleton = SingletonDatabase()

# Инициализация SQLAlchemy
engine = create_engine(db_singleton.database_url)
Base.metadata.create_all(bind=engine)


# Обработчики жизненного цикла приложения (подключение/отключение БД)
@app.on_event("startup")
async def startup():
    logger.info("Starting up...")
    await db_singleton.connect()


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down...")
    await db_singleton.disconnect()

# Регистрация роутов
app.include_router(router)
