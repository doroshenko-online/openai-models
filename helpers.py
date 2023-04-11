import os

from register import SingletonDatabase

db_singleton = SingletonDatabase()

OPENAI_ORG_ID = os.getenv('ORG_ID')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')


async def get_database():
    if not db_singleton.database.is_connected:
        await db_singleton.connect()
    return db_singleton.database


def get_openai_token():
    return OPENAI_TOKEN


def get_openai_org_id():
    return OPENAI_ORG_ID
