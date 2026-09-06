from unittest.mock import AsyncMock

from app.services.transaccion_service import TransactionsService
from app.schemas.transacciones_dto import TransactionsDTO
from app.services.evento_service import EventService
from app.schemas.eventos_dto import EventsDTO, TipoEvento


async def test_transactions_service_create_transaction_calls_repository():
    mock_repo = AsyncMock()
    mock_repo.create_transaction.return_value = "fake_id_123"

    service = TransactionsService(mock_repo)
    dto = TransactionsDTO(item="Ron", ingreso=15.5)

    result = await service.create_transaction(dto)

    assert result == "fake_id_123"
    mock_repo.create_transaction.assert_awaited_once()

    sent_dict = mock_repo.create_transaction.call_args.args[0]
    assert sent_dict["item"] == "Ron"
    assert sent_dict["ingreso"] == 15.5
    assert "fecha" in sent_dict
    assert "id" not in sent_dict


async def test_events_service_create_event_calls_repository():
    mock_repo = AsyncMock()
    mock_repo.create_event.return_value = "fake_event_id"

    service = EventService(mock_repo)
    dto = EventsDTO(tipo_evento=TipoEvento.WARNING, descripcion="Nivel bajo")

    result = await service.create_event(dto)

    assert result == "fake_event_id"
    mock_repo.create_event.assert_awaited_once()

    sent_dict = mock_repo.create_event.call_args.args[0]
    assert sent_dict["tipo_evento"] == "Warning"
    assert sent_dict["descripcion"] == "Nivel bajo"
    assert "fecha" in sent_dict
