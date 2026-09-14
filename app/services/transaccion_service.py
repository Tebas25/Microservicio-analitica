from app.repositories.transacciones_repo import TransactionsRepository
from app.schemas.transacciones_dto import TransactionsDTO, RankingDrinkDTO
from app.models.transaccion_model import TransactionsEntity


class TransactionsService:
    def __init__(self, transaction_repository: TransactionsRepository):
        self.transactions_repository = transaction_repository

    async def create_transaction(self, transaction_dto: TransactionsDTO):
        transactions = TransactionsEntity(**transaction_dto.model_dump())
        transactions_dict = transactions.model_dump(by_alias=True, exclude_none=True)
        return await self.transactions_repository.create_transaction(transactions_dict)

    async def obtain_drink_ranking(self, event_id: str, cobot_id: str) -> list:
        ranking_drinks = await self.transactions_repository.obtain_drinks_ranking(
            event_id, cobot_id
        )
        clean_ranking_drinks = list()

        for drink in ranking_drinks:
            dto = RankingDrinkDTO(drink=drink["_id"], number=drink["total"])
            clean_ranking_drinks.append(dto)

        return clean_ranking_drinks
