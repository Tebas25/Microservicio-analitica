from pymongo.asynchronous.collection import AsyncCollection
from typing import Any


class EventRepository:
    def __init__(self, collection: AsyncCollection):
        self.collection = collection

    async def create_event(self, event_data: dict[str, Any]):
        """Insertar un nuevo evento del sistema"""
        result = await self.collection.insert_one(event_data)
        return str(result.inserted_id)
