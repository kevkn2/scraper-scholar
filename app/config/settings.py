import dotenv
import os

dotenv.load_dotenv()

MENDELEY_TOKEN_URL = os.getenv("MENDELEY_TOKEN_URL", "")
SERVER_URL = os.getenv("SERVER_URL", "")
MENDELEY_CLIENT_ID = os.getenv("MENDELEY_CLIENT_ID", "")
MENDELEY_CLIENT_SECRET = os.getenv("MENDELEY_CLIENT_SECRET", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")
REDIS_HOST = os.getenv("REDIS_HOST", "")
REDIS_PORT = os.getenv("REDIS_PORT", "")
REDIS_DB = os.getenv("REDIS_DB", "")
