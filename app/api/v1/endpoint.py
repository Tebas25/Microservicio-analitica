from fastapi import APIRouter, Depends
from app.services.transaccion_service import TransactionsService
from app.schemas.transacciones_dto import TransactionsDTO
from app.services.evento_service import EventService
from app.schemas.eventos_dto import EventsDTO
from app.schemas.dashboard_response_dto import DashboardSummaryResponseDTO
from app.services.analytics_service import AnalyticsService
from app.api.dependencies import (
    get_transaction_service,
    get_events_service,
    get_analytics_service,
)

router = APIRouter()


@router.post("/transactions", status_code=201)
async def create_transactions(
    dto: TransactionsDTO,
    service: TransactionsService = Depends(get_transaction_service),
):
    result = await service.create_transaction(dto)
    return {"status": "success", "id_insertado": result}


@router.post("/events", status_code=201)
async def create_event(
    event_dto: EventsDTO, service: EventService = Depends(get_events_service)
):
    await service.create_event(event_dto)
    return {"status": "success", "message": "Evento registrado"}


@router.get("/summary")
async def obtain_transactions_metrics(
    event_id: str, service: AnalyticsService = Depends(get_analytics_service)
) -> DashboardSummaryResponseDTO:
    return await service.obtain_transaction_metrics(event_id)
