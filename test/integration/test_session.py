from app.db.session import get_databse


async def test_get_db_return():
    db = get_databse()
    assert db is not None
    assert db.name == "dbAnaliticaDesarrollo"


async def test_connection_ping():
    db = get_databse()
    result = await db.command("ping")
    assert result["ok"] == 1.0


async def test_insertar_leer_documentos():
    db = get_databse()
    collection = db.get_collection("test_integration_collection")

    document = {"campo": "valor_prueba"}
    insert_result = await collection.insert_one(document=document)
    assert insert_result.inserted_id is not None

    finded = await collection.find_one({"_id": insert_result.inserted_id})
    assert finded is not None
    assert finded["campo"] == "valor_prueba"

    await collection.delete_one({"_id": insert_result.inserted_id})
