from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OpenAIModel(Base):
    __tablename__ = "openai_models"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price = Column(Float)
