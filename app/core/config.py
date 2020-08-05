import os
from dotenv import load_dotenv
from databases import DatabaseURL

load_dotenv(dotenv_path="app/core/enviroment/.env_mongo")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 0))

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_DB = os.getenv("MONGO_DB")
PROJECT_NAME = os.getenv("PROJECT_NAME")

MONGODB_URL="mongodb://{}:{}@{}:{}/{}".format(MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DB)

database_name = MONGO_DB
owners_collection_name = "owners"


BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS")
API_STR = f"/api"
