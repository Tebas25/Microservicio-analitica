import pytest
from datetime import datetime
from bson import ObjectId
from app.models.eventos_model import EventosEntity


@pytest.mark.unit
def test_eventos_entity_defaults():
    event = EventosEntity(tipo_evento="InfoRobot", descripcion="Prueba")
    assert event.id is None
    assert isinstance(event.fecha, datetime)
    assert event.tipo_evento == "InfoRobot"


@pytest.mark.unit
def test_eventos_entity_object_id_conversion():
    oid = ObjectId()
    event = EventosEntity(_id=oid, tipo_evento="Warning", descripcion="Alerta")
    assert event.id == str(oid)
    assert isinstance(event.id, str)


@pytest.mark.unit
def test_eventos_entitu_requires_tipo_evento_descripcion():
    with pytest.raises(Exception):
        EventosEntity()
