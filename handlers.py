import logging

from databases import Database
from sqlalchemy import create_engine

from api import fetch_openai_models
from api_models import ResponseMessage, ResponseMessageGetModels, ResponseUpdateModel
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

    response = []

    query = OpenAIModel.__table__.select()
    result = await database.fetch_all(query)
    for res in result:
        response.append({
            'id': res['id'],
            'name': res['name'],
            'price': res['price']
        })

    return ResponseMessageGetModels(models=response)


async def update_model(database: Database, model_id: int, price: float = None):
    if not database.is_connected:
        await database.connect()

    columns_to_update = {}
    try:
        model_id = int(model_id)
    except (TypeError, ValueError):
        return ResponseUpdateModel(
            status="error",
            message="Invalid model id"
        )

    if price is not None:
        try:
            columns_to_update["price"] = float(price)
        except (TypeError, ValueError):
            return ResponseUpdateModel(
                status="error",
                message="Invalid price. Price must be integer"
            )

    if not columns_to_update:
        return ResponseUpdateModel(
            status="error",
            message="No fields to update"
        )

    query = OpenAIModel.__table__.update().where(OpenAIModel.id == int(model_id)).values(**columns_to_update)
    try:
        await database.execute(query)
    except Exception as e:
        logging.warning(e)
        return ResponseUpdateModel(message=f"Failed to update model with id {model_id}")
    return ResponseUpdateModel(message="Model has been updated.")
