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
        json={"item": "Ron de prueba", "ingreso": 12.0},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "id_insertado" in data


async def test_create_event_endpoint(async_client):
    response = await async_client.post(
        "/api/v1/analytics/events",
        json={"tipo_evento": "Warning", "descripcion": "Prueba de evento"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Evento registrado"
