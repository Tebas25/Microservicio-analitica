import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


async def test_create_transaction_endpoint(async_client):
    response = await async_client.post(
        "/api/v1/analytics/transactions",
        json={"evento_id": "EVT-001", "item": "Ron de prueba", "ingreso": 12.0},
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

    await async_client.post(
        "/api/v1/analytics/transactions",
        json={"item": "Ron", "ingreso": 10.0, "evento_id": event_id},
    )
    await async_client.post(
        "/api/v1/analytics/events",
        json={"tipo_evento": "Warning", "descripcion": "Prueba", "evento_id": event_id},
    )

    response = await async_client.get(
        "/api/v1/analytics/summary", params={"event_id": event_id}
    )

    assert response.status_code == 200
    data = response.json()
    assert "total_sales" in data
    assert "total_drinks_sold" in data
    assert "active_time" in data
