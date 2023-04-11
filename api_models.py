from pydantic import BaseModel


class ResponseMessage(BaseModel):
    message: str


class ResponseMessageGetModels(BaseModel):
    response: dict
