from app.repositories.transacciones_repo import TransactionsRepository
from app.schemas.dashboard_response_dto import DashboardSummaryResponseDTO
from app.repositories.eventos_repo import EventRepository


class AnalyticsService:
    def __init__(
        self,
        event_repository: EventRepository,
        transaction_repository: TransactionsRepository,
    ):
        self.event_repository = event_repository
        self.transaction_repository = transaction_repository

    async def obtain_transaction_metrics(
        self, event_id: str
    ) -> DashboardSummaryResponseDTO:
        first_date, last_date = await self.event_repository.get_active_time(event_id)

        if first_date is None or last_date is None:
            total_time = "00:00:00"
        else:
            delta = last_date - first_date
            total_seconds = int(delta.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            total_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        sales_metrics: dict = await self.transaction_repository.obtain_sales_metrics(
            event_id
        )

        return DashboardSummaryResponseDTO(
            total_sales=sales_metrics["total_sales"],
            total_drinks_sold=sales_metrics["total_drinks"],
            active_time=total_time,
        )
