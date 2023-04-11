from fastapi import APIRouter

from api_models import ResponseMessage, ResponseMessageGetModels
from handlers import get_models, sync_models, update_model
from helpers import get_database

router = APIRouter()


@router.get("/sync_models", response_model=ResponseMessage)
async def sync_openai_models():
    return await sync_models(await get_database())


@router.get("/get_models", response_model=ResponseMessageGetModels)
async def sync_openai_models():
    return await get_models(await get_database())


@router.put("/update_model/{model_id}", response_model=str)
async def update_openai_model(model_id: int, name: str = None, price: float = None):
    return await update_model(await get_database(), model_id, name, price)
