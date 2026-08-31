import pytest
from pydantic import ValidationError
from app.schemas.transacciones_dto import TransaccionesDTO


@pytest.mark.unit
def test_transacciones_dto_valido():
    dto = TransaccionesDTO(item="Ron", ingreso=10.0)
    assert dto.item == "Ron"
    assert dto.ingreso == 10.0


@pytest.mark.unit
def test_transacciones_dto_ingreso_negativo_falla():
    with pytest.raises(ValidationError):
        TransaccionesDTO(item="Ron", ingreso=-5.0)


@pytest.mark.unit
def test_transacciones_dto_item_muy_corto_falla():
    with pytest.raises(ValidationError):
        TransaccionesDTO(item="ab", ingreso=10.0)


@pytest.mark.unit
def test_transacciones_dto_item_muy_largo_falla():
    with pytest.raises(ValidationError):
        TransaccionesDTO(item="a" * 51, ingreso=10.0)
