from pymongo.asynchronous.collection import AsyncCollection
from typing import Any


class TransactionsRepository:
    def __init__(self, collection: AsyncCollection):
        self.collection = collection

    async def create_transaction(self, transactions_data: dict[str, Any]):
        """Insertar una nueva transacciones y devuelve su Id en formato string"""
        result = await self.collection.insert_one(transactions_data)
        return str(result.inserted_id)

    async def obtain_sales_metrics(self, event_id: str) -> dict:
        """
        Obtener un resumen de ventas totales (USD)
        Obtener el total de bebidas servidas.
        Obtener el tiempo total de actividad del COBOT JAKA
        Obtener el último evento registrado, si es actividad normal o si ocurrió un errro en el sistema
        """
        pipeline = [
            {"$match": {"evento_id": event_id}},
            {
                "$facet": {
                    "sales": [
                        {"$group": {"_id": None, "total": {"$sum": "$ingreso"}}},
                        {"$project": {"total": {"$round": ["$total", 2]}}},
                    ],
                    "drinks_count": [{"$count": "total"}],
                }
            },
        ]

        cursor = await self.collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)

        facet = result[0] if result else {"sales": [], "drink_count": []}
        total_sales = facet["sales"][0]["total"] if facet["sales"] else 0.0
        total_drinks = facet["drinks_count"][0]["total"] if facet["drinks_count"] else 0

        return {"total_sales": total_sales, "total_drinks": total_drinks}
