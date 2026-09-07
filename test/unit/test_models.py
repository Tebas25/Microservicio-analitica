import pytest
from datetime import datetime
from bson import ObjectId

from app.models.eventos_model import EventsEntity
from app.models.transaccion_model import TransactionsEntity

# ---------------------------------------------------------------------------
# EventsEntity
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_eventos_entity_defaults():
    event = EventsEntity(
        evento_id="EVT-001", tipo_evento="InfoRobot", descripcion="Prueba"
    )
    assert event.id is None
    assert isinstance(event.fecha, datetime)
    assert event.evento_id == "EVT-001"
    assert event.tipo_evento == "InfoRobot"


@pytest.mark.unit
def test_eventos_entity_object_id_conversion():
    oid = ObjectId()
    event = EventsEntity(
        _id=oid, evento_id="EVT-001", tipo_evento="Warning", descripcion="Alerta"
    )
    assert event.id == str(oid)
    assert isinstance(event.id, str)


@pytest.mark.unit
def test_eventos_entity_requires_tipo_evento_descripcion():
    with pytest.raises(Exception):
        EventsEntity(evento_id="EVT-001")


# ---------------------------------------------------------------------------
# TransactionsEntity
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_transacciones_entity_defaults():
    tx = TransactionsEntity(evento_id="EVT-001", item="Ron", ingreso=12.30)
    assert tx.id is None
    assert isinstance(tx.fecha, datetime)
    assert tx.evento_id == "EVT-001"
    assert tx.item == "Ron"
    assert tx.ingreso == 12.30


@pytest.mark.unit
def test_transacciones_entity_object_id_conversion():
    oid = ObjectId()
    tx = TransactionsEntity(_id=oid, evento_id="EVT-001", item="Vodka", ingreso=14.0)
    assert tx.id == str(oid)


@pytest.mark.unit
def test_transacciones_entity_requires_item():
    with pytest.raises(Exception):
        TransactionsEntity(evento_id="EVT-001", ingreso=10.0)
