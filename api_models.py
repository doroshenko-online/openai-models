from pydantic import BaseModel


class ResponseMessage(BaseModel):
    message: str


class ResponseMessageGetModels(BaseModel):
    models: list[dict]


class ResponseUpdateModel(BaseModel):
    status: str = 'success'
    message: str
