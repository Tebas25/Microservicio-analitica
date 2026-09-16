from app.core.config import settings
from pymongo import AsyncMongoClient

client = AsyncMongoClient(settings.CONNECTION_STRING)
db = client.dbAnaliticaDesarrollo


def get_databse():
    return db
