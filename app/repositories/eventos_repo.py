from pymongo.asynchronous.collection import AsyncCollection
from typing import Any


class EventRepository:
    def __init__(self, collection: AsyncCollection):
        self.collection = collection

    async def create_event(self, event_data: dict[str, Any]):
        """Insertar un nuevo evento del sistema"""
        result = await self.collection.insert_one(event_data)
        return str(result.inserted_id)

    async def get_active_time(self, event_id: str):
        """
        Obtener todas las fechas, odernardas de forma ascendente y forma descendente y retorna dos valores,
        uno de la primera fecha y otro de la última fecha
        """
        first_date = (
            self.collection.find({"evento_id": event_id}).sort("fecha", 1).limit(1)
        )
        last_date = (
            self.collection.find({"evento_id": event_id}).sort("fecha", -1).limit(1)
        )

        first_docs = await first_date.to_list(length=1)
        last_docs = await last_date.to_list(length=1)

        if not first_docs or not last_docs:
            return None, None

        return first_docs[0]["fecha"], last_docs[0]["fecha"]
