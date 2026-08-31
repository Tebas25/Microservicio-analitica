import pytest
from datetime import datetime
from bson import ObjectId
from app.models.transaccion_model import TransaccionesEntity


@pytest.mark.unit
def test_transacciones_entitu_defaults():
    tx = TransaccionesEntity(item="Ron", ingreso=12.30)
    assert tx.id is None
    assert isinstance(tx.fecha, datetime)
    assert tx.item == "Ron"
    assert tx.ingreso == 12.30


@pytest.mark.unit
def test_trasacciones_entity_object_id_conversion():
    oid = ObjectId
    tx = TransaccionesEntity(_id=oid, item="Vodka", ingreso=14.0)
    assert tx.id == str(oid)
