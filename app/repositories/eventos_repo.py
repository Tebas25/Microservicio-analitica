from pymongo.asynchronous.collection import AsyncCollection
from typing import Any
from typing import Any, Optional
from datetime import datetime

from app.schemas.eventos_dto import TipoEvento


class EventRepository:
    def __init__(self, collection: AsyncCollection):
        self.collection = collection

    async def create_event(self, event_data: dict[str, Any]):
        """Insertar un nuevo evento del sistema"""
        result = await self.collection.insert_one(event_data)
        return str(result.inserted_id)

    async def get_active_time(self, event_id: str, cobot_id: str):
        """
        Obtener todas las fechas, odernardas de forma ascendente y forma descendente y retorna dos valores,
        uno de la primera fecha y otro de la última fecha
        """
        first_date = (
            self.collection.find({"evento_id": event_id, "cobot_id": cobot_id})
            .sort("fecha", 1)
            .limit(1)
        )
        last_date = (
            self.collection.find({"evento_id": event_id, "cobot_id": cobot_id})
            .sort("fecha", -1)
            .limit(1)
        )

        first_docs = await first_date.to_list(length=1)
        last_docs = await last_date.to_list(length=1)

        if not first_docs or not last_docs:
            return None, None

        return first_docs[0]["fecha"], last_docs[0]["fecha"]

    async def get_events_filtered(
        self,
        cobot_id: str,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        tipos_evento: Optional[list[TipoEvento]] = None,
    ) -> list[dict[str, Any]]:
        query: dict[str, Any] = {"cobot_id": cobot_id}

        if fecha_inicio or fecha_fin:
            fecha_filter: dict[str, Any] = {}
            if fecha_inicio:
                fecha_filter["$gte"] = fecha_inicio
            if fecha_fin:
                fecha_filter["$lte"] = fecha_fin
            query["fecha"] = fecha_filter

        if tipos_evento:
            # Convertimos los Enum a sus valores string planos para evitar
            # problemas de serialización BSON
            query["tipo_evento"] = {"$in": [t.value for t in tipos_evento]}

        cursor = self.collection.find(query).sort("fecha", -1)
        return await cursor.to_list(length=None)
