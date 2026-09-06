import pytest
from pydantic import ValidationError
from app.schemas.eventos_dto import EventsDTO, TipoEvento


@pytest.mark.unit
def test_eventos_dto_valid():
    dto = EventsDTO(tipo_evento="Warning", descripcion="Nivel Bajo")
    assert dto.tipo_evento == TipoEvento.WARNING


@pytest.mark.unit
def test_eventos_dto_evento_invalido():
    with pytest.raises(Exception):
        EventsDTO(tipo_evento="TipoInexistente", descripcion="Algo")


@pytest.mark.unit
@pytest.mark.parametrize("tipo", list(TipoEvento))
def test_eventos_dto_acepta_todos_enum(tipo):
    dto = EventsDTO(tipo_evento=tipo, descripcion="Test")
    assert dto.tipo_evento == tipo
