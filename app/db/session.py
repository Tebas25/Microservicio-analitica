from app.core.config import settings
from pymongo import AsyncMongoClient

client = AsyncMongoClient(settings.CONNECTION_STRING)
db = client.dbAnalisisDesarrollo


def get_databse():
    return db
