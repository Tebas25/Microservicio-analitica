from datetime import datetime, timezone

import pytest
from httpx import AsyncClient, ASGITransport
from app.db.session import get_databse
from app.main import app


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


async def test_create_transaction_endpoint(async_client):
    response = await async_client.post(
        "/api/v1/analytics/transactions",
        json={
            "evento_id": "EVT-001",
            "cobot_id": "COBOT-01",
            "item": "Ron de prueba",
            "ingreso": 12.0,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "id_insertado" in data


async def test_create_event_endpoint(async_client):
    response = await async_client.post(
        "/api/v1/analytics/events",
        json={
            "evento_id": "EVT-001",
            "cobot_id": "COBOT-01",
            "tipo_evento": "Warning",
            "descripcion": "Prueba de evento",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Evento registrado"


async def test_get_summary_endpoint(async_client):
    event_id = "TEST-SUMMARY-EVT"
    cobot_id = "COBOT-01"

    await async_client.post(
        "/api/v1/analytics/transactions",
        json={
            "evento_id": event_id,
            "cobot_id": cobot_id,
            "item": "Ron",
            "ingreso": 10.0,
        },
    )
    await async_client.post(
        "/api/v1/analytics/events",
        json={
            "evento_id": event_id,
            "cobot_id": cobot_id,
            "tipo_evento": "Warning",
            "descripcion": "Prueba",
        },
    )

    response = await async_client.get(
        f"/api/v1/analytics/summary/{cobot_id}", params={"event_id": event_id}
    )

    assert response.status_code == 200
    data = response.json()
    assert "total_sales" in data
    assert "total_drinks_sold" in data
    assert "active_time" in data


async def test_get_drinks_ranking_endpoint(async_client):
    event_id = "TEST-RANKING-EVT"
    cobot_id = "COBOT-TEST"

    await async_client.post(
        "/api/v1/analytics/transactions",
        json={
            "evento_id": event_id,
            "cobot_id": cobot_id,
            "item": "Ron",
            "ingreso": 10.0,
        },
    )
    await async_client.post(
        "/api/v1/analytics/transactions",
        json={
            "evento_id": event_id,
            "cobot_id": cobot_id,
            "item": "Ron",
            "ingreso": 8.0,
        },
    )

    response = await async_client.get(
        f"/api/v1/analytics/drinks-ranking/{cobot_id}", params={"event_id": event_id}
    )

    assert response.status_code == 200
    data = response.json()
    assert data[0]["drink"] == "Ron"
    assert data[0]["number"] == 2

    db = get_databse()
    await db.get_collection("transacciones").delete_many({"evento_id": event_id})

# ---------------------------------------------------------------------------
# GET /api/v1/analytics/get-events
# ---------------------------------------------------------------------------

GET_EVENTS_PATH = "/api/v1/analytics/get-events"

# AJUSTA este nombre al de la colección real que usa tu app en producción
# (la misma que consulta get_events_service -> EventRepository).
EVENTOS_COLLECTION_NAME = "eventos"

def _eventos_de_prueba_endpoint():
    """
    Documentos insertados directamente en la colección (no vía el endpoint
    de creación, porque este último no acepta cobot_id/fecha en su payload).
    """
    return [
        {
            "evento_id": "EVT-ENDPOINT-1",
            "cobot_id": "cobot-endpoint",
            "fecha": datetime(2026, 9, 1, 8, 0, 0, tzinfo=timezone.utc),
            "tipo_evento": "InfoRobot",
            "descripcion": "cobot-endpoint InfoRobot dia 1",
        },
        {
            "evento_id": "EVT-ENDPOINT-2",
            "cobot_id": "cobot-endpoint",
            "fecha": datetime(2026, 9, 5, 12, 0, 0, tzinfo=timezone.utc),
            "tipo_evento": "Warning",
            "descripcion": "cobot-endpoint Warning dia 5",
        },
        {
            "evento_id": "EVT-ENDPOINT-3",
            "cobot_id": "cobot-endpoint-otro",
            "fecha": datetime(2026, 9, 5, 12, 0, 0, tzinfo=timezone.utc),
            "tipo_evento": "Warning",
            "descripcion": "otro cobot, mismo dia",
        },
    ]


@pytest.fixture
async def eventos_insertados():
    """Inserta eventos de prueba en la colección real y los limpia al final."""
    db = get_databse()
    collection = db.get_collection(EVENTOS_COLLECTION_NAME)

    documentos = _eventos_de_prueba_endpoint()
    await collection.insert_many(documentos)

    yield documentos

    await collection.delete_many(
        {"evento_id": {"$in": [doc["evento_id"] for doc in documentos]}}
    )


async def test_get_events_requiere_cobot_id(async_client):
    response = await async_client.get(GET_EVENTS_PATH)
    assert response.status_code == 422


async def test_get_events_devuelve_solo_los_del_cobot_id(
        async_client, eventos_insertados
):
    response = await async_client.get(
        GET_EVENTS_PATH, params={"cobot_id": "cobot-endpoint"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(evento["cobot_id"] == "cobot-endpoint" for evento in data)


async def test_get_events_filtra_por_tipo_evento(async_client, eventos_insertados):
    response = await async_client.get(
        GET_EVENTS_PATH,
        params={"cobot_id": "cobot-endpoint", "tipo_evento": "InfoRobot"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["evento_id"] == "EVT-ENDPOINT-1"


async def test_get_events_multiples_tipo_evento(async_client, eventos_insertados):
    response = await async_client.get(
        GET_EVENTS_PATH,
        params=[
            ("cobot_id", "cobot-endpoint"),
            ("tipo_evento", "InfoRobot"),
            ("tipo_evento", "Warning"),
        ],
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


async def test_get_events_filtra_por_rango_de_fechas(async_client, eventos_insertados):
    response = await async_client.get(
        GET_EVENTS_PATH,
        params={
            "cobot_id": "cobot-endpoint",
            "fecha_inicio": "2026-09-04T00:00:00Z",
            "fecha_fin": "2026-09-09T00:00:00Z",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["evento_id"] == "EVT-ENDPOINT-2"


async def test_get_events_tipo_evento_invalido_devuelve_422(async_client):
    response = await async_client.get(
        GET_EVENTS_PATH,
        params={"cobot_id": "cobot-endpoint", "tipo_evento": "NoExiste"},
    )
    assert response.status_code == 422


async def test_get_events_cobot_sin_eventos_devuelve_lista_vacia(
        async_client, eventos_insertados
):
    response = await async_client.get(
        GET_EVENTS_PATH, params={"cobot_id": "cobot-sin-eventos"}
    )

    assert response.status_code == 200
    assert response.json() == []


async def test_get_events_respuesta_solo_tiene_campos_del_dto(
        async_client, eventos_insertados
):
    response = await async_client.get(
        GET_EVENTS_PATH, params={"cobot_id": "cobot-endpoint"}
    )

    data = response.json()[0]
    assert set(data.keys()) == {
        "cobot_id",
        "fecha",
        "evento_id",
        "tipo_evento",
        "descripcion",
    }