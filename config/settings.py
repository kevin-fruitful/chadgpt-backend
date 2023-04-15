import os
from dotenv import load_dotenv

load_dotenv()

# Flask settings
FLASK_CONFIG = os.getenv("FLASK_CONFIG", "config.default")

# Database settings
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")

# Other settings, e.g. secret keys, API keys, etc.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "openai_api_key")
