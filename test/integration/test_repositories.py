from datetime import datetime, timezone
from unittest.mock import MagicMock, AsyncMock

import pytest

from app.db.session import get_databse
from app.repositories.transacciones_repo import TransactionsRepository
from app.repositories.eventos_repo import EventRepository
from app.schemas.eventos_dto import TipoEvento


async def test_transactions_repository_insert():
    db = get_databse()
    collection = db.get_collection("test_transactions_repo")
    repo = TransactionsRepository(collection)

    data = {"evento_id": "EVT-001", "item": "Vodka", "ingreso": 20.0}
    inserted_id = await repo.create_transaction(data)

    assert inserted_id is not None
    found = await collection.find_one({"item": "Vodka"})
    assert found is not None
    assert found["ingreso"] == 20.0

    await collection.delete_one({"item": "Vodka"})


async def test_event_repository_insert():
    db = get_databse()
    collection = db.get_collection("test_events_repo")
    repo = EventRepository(collection)

    data = {
        "evento_id": "EVT-001",
        "tipo_evento": "Warning",
        "descripcion": "Nivel bajo de stock",
    }
    inserted_id = await repo.create_event(data)

    assert inserted_id is not None
    found = await collection.find_one({"tipo_evento": "Warning"})
    assert found is not None
    assert found["descripcion"] == "Nivel bajo de stock"

    await collection.delete_one({"tipo_evento": "Warning"})


async def test_transactions_repository_sales_metrics():
    db = get_databse()
    collection = db.get_collection("test_transactions_sales")
    repo = TransactionsRepository(collection)

    await collection.insert_many(
        [
            {"evento_id": "TEST-EVT", "item": "Ron", "ingreso": 10.0},
            {"evento_id": "TEST-EVT", "item": "Vodka", "ingreso": 5.0},
        ]
    )

    metrics = await repo.obtain_sales_metrics("TEST-EVT")

    assert metrics["total_sales"] == 15.0
    assert metrics["total_drinks"] == 2

    await collection.delete_many({"evento_id": "TEST-EVT"})


async def test_event_repository_get_active_time():
    db = get_databse()
    collection = db.get_collection("test_events_active_time")
    repo = EventRepository(collection)

    await collection.insert_many(
        [
            {
                "evento_id": "TEST-EVT",
                "fecha": datetime(2026, 9, 6, 10, 0, 0, tzinfo=timezone.utc),
                "tipo_evento": "InfoRobot",
                "descripcion": "inicio",
            },
            {
                "evento_id": "TEST-EVT",
                "fecha": datetime(2026, 9, 6, 11, 0, 0, tzinfo=timezone.utc),
                "tipo_evento": "InfoRobot",
                "descripcion": "fin",
            },
        ]
    )

    first_date, last_date = await repo.get_active_time("TEST-EVT")

    assert first_date is not None
    assert last_date is not None
    assert (last_date - first_date).total_seconds() == 3600

    await collection.delete_many({"evento_id": "TEST-EVT"})


# ---------------------------------------------------------------------------
# EventRepository.get_events_filtered
# ---------------------------------------------------------------------------


def _eventos_de_prueba():
    """Set de documentos para probar filtros de cobot_id, fecha y tipo_evento."""
    return [
        {
            "evento_id": "EVT-FILTRO-1",
            "cobot_id": "cobot-A",
            "fecha": datetime(2026, 9, 1, 8, 0, 0, tzinfo=timezone.utc),
            "tipo_evento": "InfoRobot",
            "descripcion": "cobot-A InfoRobot dia 1",
        },
        {
            "evento_id": "EVT-FILTRO-2",
            "cobot_id": "cobot-A",
            "fecha": datetime(2026, 9, 5, 12, 0, 0, tzinfo=timezone.utc),
            "tipo_evento": "Warning",
            "descripcion": "cobot-A Warning dia 5",
        },
        {
            "evento_id": "EVT-FILTRO-3",
            "cobot_id": "cobot-A",
            "fecha": datetime(2026, 9, 10, 9, 0, 0, tzinfo=timezone.utc),
            "tipo_evento": "ErrorRobot",
            "descripcion": "cobot-A ErrorRobot dia 10",
        },
        {
            "evento_id": "EVT-FILTRO-4",
            "cobot_id": "cobot-B",
            "fecha": datetime(2026, 9, 5, 12, 0, 0, tzinfo=timezone.utc),
            "tipo_evento": "Warning",
            "descripcion": "cobot-B Warning dia 5 (otro cobot)",
        },
    ]


async def test_event_repository_get_events_filtered_por_cobot_id():
    db = get_databse()
    collection = db.get_collection("test_events_filtered_cobot")
    repo = EventRepository(collection)

    await collection.insert_many(_eventos_de_prueba())

    resultados = await repo.get_events_filtered(cobot_id="cobot-A")

    assert len(resultados) == 3
    assert all(evento["cobot_id"] == "cobot-A" for evento in resultados)

    await collection.delete_many({"evento_id": {"$in": [
        "EVT-FILTRO-1", "EVT-FILTRO-2", "EVT-FILTRO-3", "EVT-FILTRO-4"
    ]}})


async def test_event_repository_get_events_filtered_por_rango_fechas():
    db = get_databse()
    collection = db.get_collection("test_events_filtered_fechas")
    repo = EventRepository(collection)

    await collection.insert_many(_eventos_de_prueba())

    resultados = await repo.get_events_filtered(
        cobot_id="cobot-A",
        fecha_inicio=datetime(2026, 9, 4, tzinfo=timezone.utc),
        fecha_fin=datetime(2026, 9, 9, tzinfo=timezone.utc),
    )

    assert len(resultados) == 1
    assert resultados[0]["evento_id"] == "EVT-FILTRO-2"

    await collection.delete_many({"evento_id": {"$in": [
        "EVT-FILTRO-1", "EVT-FILTRO-2", "EVT-FILTRO-3", "EVT-FILTRO-4"
    ]}})


async def test_event_repository_get_events_filtered_por_tipo_evento():
    db = get_databse()
    collection = db.get_collection("test_events_filtered_tipo")
    repo = EventRepository(collection)

    await collection.insert_many(_eventos_de_prueba())

    resultados = await repo.get_events_filtered(
        cobot_id="cobot-A",
        tipos_evento=[TipoEvento.INFO_ROBOT, TipoEvento.ERROR_ROBOT],
    )

    tipos_encontrados = {evento["tipo_evento"] for evento in resultados}
    assert len(resultados) == 2
    assert tipos_encontrados == {"InfoRobot", "ErrorRobot"}

    await collection.delete_many({"evento_id": {"$in": [
        "EVT-FILTRO-1", "EVT-FILTRO-2", "EVT-FILTRO-3", "EVT-FILTRO-4"
    ]}})


async def test_event_repository_get_events_filtered_sin_tipo_trae_todos():
    db = get_databse()
    collection = db.get_collection("test_events_filtered_sin_tipo")
    repo = EventRepository(collection)

    await collection.insert_many(_eventos_de_prueba())

    resultados = await repo.get_events_filtered(cobot_id="cobot-A", tipos_evento=[])

    assert len(resultados) == 3

    await collection.delete_many({"evento_id": {"$in": [
        "EVT-FILTRO-1", "EVT-FILTRO-2", "EVT-FILTRO-3", "EVT-FILTRO-4"
    ]}})


async def test_event_repository_get_events_filtered_ordena_por_fecha_descendente():
    db = get_databse()
    collection = db.get_collection("test_events_filtered_orden")
    repo = EventRepository(collection)

    await collection.insert_many(_eventos_de_prueba())

    resultados = await repo.get_events_filtered(cobot_id="cobot-A")

    fechas = [evento["fecha"] for evento in resultados]
    assert fechas == sorted(fechas, reverse=True)

    await collection.delete_many({"evento_id": {"$in": [
        "EVT-FILTRO-1", "EVT-FILTRO-2", "EVT-FILTRO-3", "EVT-FILTRO-4"
    ]}})


async def test_event_repository_get_events_filtered_cobot_sin_eventos():
    db = get_databse()
    collection = db.get_collection("test_events_filtered_vacio")
    repo = EventRepository(collection)

    await collection.insert_many(_eventos_de_prueba())

    resultados = await repo.get_events_filtered(cobot_id="cobot-inexistente")

    assert resultados == []

    await collection.delete_many({"evento_id": {"$in": [
        "EVT-FILTRO-1", "EVT-FILTRO-2", "EVT-FILTRO-3", "EVT-FILTRO-4"
    ]}})