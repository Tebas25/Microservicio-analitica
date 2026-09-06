from datetime import datetime, timezone
from app.db.session import get_databse
from app.repositories.transacciones_repo import TransactionsRepository
from app.repositories.eventos_repo import EventRepository


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
