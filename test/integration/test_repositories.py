from app.db.session import get_databse
from app.repositories.transacciones_repo import TransactionsRepository
from app.repositories.eventos_repo import EventRepository


async def test_transactions_repository_insert():
    db = get_databse()
    collection = db.get_collection("test_transactions_repo")
    repo = TransactionsRepository(collection)

    data = {"item": "Vodka", "ingreso": 20.0}
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

    data = {"tipo_evento": "Warning", "descripcion": "Nivel bajo de stock"}
    inserted_id = await repo.create_event(data)

    assert inserted_id is not None
    found = await collection.find_one({"tipo_evento": "Warning"})
    assert found is not None
    assert found["descripcion"] == "Nivel bajo de stock"

    await collection.delete_one({"tipo_evento": "Warning"})
