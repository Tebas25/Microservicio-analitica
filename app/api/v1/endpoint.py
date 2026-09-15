from fastapi import APIRouter, Depends

from app.repositories.eventos_repo import EventRepository
from app.services.transaccion_service import TransactionsService
from app.schemas.transacciones_dto import TransactionsDTO
from app.services.evento_service import EventService
from app.schemas.eventos_dto import EventsDTO, EventosResponseDTO, TipoEvento
from app.schemas.dashboard_response_dto import DashboardSummaryResponseDTO
from app.services.analytics_service import AnalyticsService
from app.api.dependencies import (
    get_transaction_service,
    get_events_service,
    get_analytics_service,
)

from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query

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


@router.get("/summary/{cobot_id}")
async def obtain_transactions_metrics(
    event_id: str,
    cobot_id: str,
    service: AnalyticsService = Depends(get_analytics_service),
) -> DashboardSummaryResponseDTO:
    return await service.obtain_transaction_metrics(event_id, cobot_id)


@router.get("/drinks-ranking/{cobot_id}")
async def obtain_drinks_ranking(
    cobot_id: str,
    event_id: str,
    service: TransactionsService = Depends(get_transaction_service),
) -> list:
    return await service.obtain_drink_ranking(event_id, cobot_id)


@router.get("/get-events", response_model=list[EventosResponseDTO])
async def listar_eventos(
    cobot_id: str = Query(...),
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    tipo_evento: Optional[list[TipoEvento]] = Query(None),
    service: EventService = Depends(get_events_service),
):
    events = await service.event_repository.get_events_filtered(
        cobot_id=cobot_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        tipos_evento=tipo_evento,
    )
    return events
