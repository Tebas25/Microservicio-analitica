from pymongo.asynchronous.collection import AsyncCollection
from typing import Any


class TransactionsRepository:
    def __init__(self, collection: AsyncCollection):
        self.collection = collection

    async def create_transaction(self, transactions_data: dict[str, Any]):
        """Insertar una nueva transacciones y devuelve su Id en formato string"""
        result = await self.collection.insert_one(transactions_data)
        return str(result.inserted_id)
