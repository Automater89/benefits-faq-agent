"""
config.py -- Load and validate environment variables.
Run directly to test Azure service connectivity.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def get_config() -> dict:
    required_keys = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_KEY",
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
        "AZURE_AI_SEARCH_ENDPOINT",
        "AZURE_AI_SEARCH_KEY",
        "AZURE_AI_SEARCH_INDEX_NAME",
        "AZURE_STORAGE_CONNECTION_STRING",
        "AZURE_STORAGE_CONTAINER",
    ]
    config = {}
    missing = []
    for key in required_keys:
        value = os.getenv(key)
        if not value:
            missing.append(key)
        config[key] = value
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {missing}")
    return config


if __name__ == "__main__":
    try:
        cfg = get_config()
        print("[OK] All environment variables loaded.")
        print(f"  OpenAI endpoint   : {cfg['AZURE_OPENAI_ENDPOINT']}")
        print(f"  Search endpoint   : {cfg['AZURE_AI_SEARCH_ENDPOINT']}")
        print(f"  Storage container : {cfg['AZURE_STORAGE_CONTAINER']}")
    except EnvironmentError as e:
        print(f"[ERROR] {e}")
