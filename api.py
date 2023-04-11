import logging
import openai

from helpers import get_openai_token

logger = logging.getLogger(__name__)
openai.api_key = get_openai_token()


def fetch_openai_models():
    try:
        response = openai.Engine.list()
        return response["data"]
    except Exception as e:
        logger.error(f"Request failed: {e}")
        raise
