import logging

from databases import Database
from sqlalchemy import create_engine

from api import fetch_openai_models
from api_models import ResponseMessage, ResponseMessageGetModels
from models import OpenAIModel
from sqlalchemy.orm import sessionmaker

from register import SingletonDatabase

logger = logging.getLogger(__name__)


async def sync_models(database: Database) -> ResponseMessage:
    if not database.is_connected:
        await database.connect()
    models = fetch_openai_models()

    # Создаем сессию с явным подключением к базе данных
    db_singleton = SingletonDatabase()
    engine = create_engine(db_singleton.database_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Очистить таблицу перед добавлением новых данных
    async with database.transaction():
        query = OpenAIModel.__table__.delete()
        await database.execute(query)

    for model in models:
        new_model = OpenAIModel(name=model["id"])
        session.add(new_model)

    session.commit()
    session.close()

    logger.info("OpenAI models have been synchronized.")
    return ResponseMessage(message="Models synced successfully")


async def get_models(database: Database) -> ResponseMessageGetModels:
    if not database.is_connected:
        await database.connect()

    response = {}

    query = OpenAIModel.__table__.select()
    result = await database.fetch_all(query)
    print(result)
    for res in result:
        response[res['name']] = res['price']

    return ResponseMessageGetModels(response=response)


async def update_model(database: Database, model_id: int, name: str = None, price: float = None):
    columns_to_update = {}

    if name is not None:
        columns_to_update["name"] = name
    if price is not None:
        columns_to_update["price"] = price

    query = OpenAIModel.__table__.update().where(OpenAIModel.id == model_id).values(**columns_to_update)
    result = await database.execute(query)

    if result:
        logger.info(f"Model {model_id} has been updated.")
        return {"status": "success", "message": "Model has been updated."}
    else:
        logger.error(f"Failed to update model {model_id}.")
        return {"status": "error", "message": "Failed to update model."}
