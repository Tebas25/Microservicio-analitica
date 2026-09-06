from fastapi.testclient import TestClient
from app.main import app


def test_create_transaction_endpoint():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/analytics/transactions",
            json={"item": "Ron de prueba", "ingreso": 12.0},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "id_insertado" in data


def test_create_event_endpoint():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/analytics/events",
            json={"tipo_evento": "Warning", "descripcion": "Prueba de evento"},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Evento registrado"
