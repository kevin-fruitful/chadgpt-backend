import os
from dotenv import load_dotenv

load_dotenv()

# Flask settings
FLASK_CONFIG = os.getenv("FLASK_CONFIG", "config.default")

# Other settings, e.g. secret keys, API keys, etc.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "openai_api_key")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "pinecone_api_key")

PINECONE_ENV = os.getenv("PINECONE_ENV", "pinecone_env")
