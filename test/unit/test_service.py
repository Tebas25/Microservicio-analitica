from unittest.mock import AsyncMock
from datetime import datetime, timezone, timedelta

from app.services.transaccion_service import TransactionsService
from app.schemas.transacciones_dto import TransactionsDTO
from app.services.evento_service import EventService
from app.schemas.eventos_dto import EventsDTO, TipoEvento
from app.services.analytics_service import AnalyticsService


async def test_transactions_service_create_transaction_calls_repository():
    mock_repo = AsyncMock()
    mock_repo.create_transaction.return_value = "fake_id_123"

    service = TransactionsService(mock_repo)
    dto = TransactionsDTO(evento_id="EVT-001", item="Ron", ingreso=15.5)

    result = await service.create_transaction(dto)

    assert result == "fake_id_123"
    mock_repo.create_transaction.assert_awaited_once()

    sent_dict = mock_repo.create_transaction.call_args.args[0]
    assert sent_dict["evento_id"] == "EVT-001"
    assert sent_dict["item"] == "Ron"
    assert sent_dict["ingreso"] == 15.5
    assert "fecha" in sent_dict
    assert "id" not in sent_dict


async def test_events_service_create_event_calls_repository():
    mock_repo = AsyncMock()
    mock_repo.create_event.return_value = "fake_event_id"

    service = EventService(mock_repo)
    dto = EventsDTO(
        evento_id="EVT-001", tipo_evento=TipoEvento.WARNING, descripcion="Nivel bajo"
    )

    result = await service.create_event(dto)

    assert result == "fake_event_id"
    mock_repo.create_event.assert_awaited_once()

    sent_dict = mock_repo.create_event.call_args.args[0]
    assert sent_dict["evento_id"] == "EVT-001"
    assert sent_dict["tipo_evento"] == "Warning"
    assert sent_dict["descripcion"] == "Nivel bajo"
    assert "fecha" in sent_dict


async def test_analytics_service_calculates_active_time_and_sales():
    mock_event_repo = AsyncMock()
    mock_transaction_repo = AsyncMock()

    start = datetime(2026, 9, 6, 10, 0, 0, tzinfo=timezone.utc)
    end = start + timedelta(hours=1, minutes=30, seconds=15)
    mock_event_repo.get_active_time.return_value = (start, end)
    mock_transaction_repo.obtain_sales_metrics.return_value = {
        "total_sales": 100.5,
        "total_drinks": 10,
    }

    service = AnalyticsService(
        event_repository=mock_event_repo,
        transaction_repository=mock_transaction_repo,
    )

    result = await service.obtain_transaction_metrics("EVT-001")

    assert result.total_sales == 100.5
    assert result.total_drinks_sold == 10
    assert result.active_time == "01:30:15"


async def test_analytics_service_handles_missing_dates():
    mock_event_repo = AsyncMock()
    mock_transaction_repo = AsyncMock()

    mock_event_repo.get_active_time.return_value = (None, None)
    mock_transaction_repo.obtain_sales_metrics.return_value = {
        "total_sales": 0.0,
        "total_drinks": 0,
    }

    service = AnalyticsService(
        event_repository=mock_event_repo,
        transaction_repository=mock_transaction_repo,
    )

    result = await service.obtain_transaction_metrics("EVT-999")

    assert result.active_time == "00:00:00"
