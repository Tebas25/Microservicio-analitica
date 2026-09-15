from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.schemas.eventos_dto import EventsDTO, TipoEvento, EventosResponseDTO
from app.schemas.transacciones_dto import TransactionsDTO
from app.schemas.dashboard_response_dto import DashboardSummaryResponseDTO

# ---------------------------------------------------------------------------
# EventsDTO
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_eventos_dto_valido():
    dto = EventsDTO(
        evento_id="EVT-001", tipo_evento="Warning", descripcion="Nivel Bajo"
    )
    assert dto.evento_id == "EVT-001"
    assert dto.tipo_evento == TipoEvento.WARNING


@pytest.mark.unit
def test_eventos_dto_evento_invalido():
    with pytest.raises(ValidationError):
        EventsDTO(
            evento_id="EVT-001", tipo_evento="TipoInexistente", descripcion="Algo"
        )


@pytest.mark.unit
def test_eventos_dto_requiere_evento_id():
    with pytest.raises(ValidationError):
        EventsDTO(tipo_evento="Warning", descripcion="Algo")


@pytest.mark.unit
@pytest.mark.parametrize("tipo", list(TipoEvento))
def test_eventos_dto_acepta_todos_enum(tipo):
    dto = EventsDTO(evento_id="EVT-001", tipo_evento=tipo, descripcion="Test")
    assert dto.tipo_evento == tipo


# ---------------------------------------------------------------------------
# TransactionsDTO
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_transacciones_dto_valido():
    dto = TransactionsDTO(evento_id="EVT-001", item="Ron", ingreso=10.0)
    assert dto.evento_id == "EVT-001"
    assert dto.item == "Ron"
    assert dto.ingreso == 10.0


@pytest.mark.unit
def test_transacciones_dto_requiere_evento_id():
    with pytest.raises(ValidationError):
        TransactionsDTO(item="Ron", ingreso=10.0)


@pytest.mark.unit
def test_transacciones_dto_ingreso_negativo_falla():
    with pytest.raises(ValidationError):
        TransactionsDTO(evento_id="EVT-001", item="Ron", ingreso=-5.0)


@pytest.mark.unit
def test_transacciones_dto_item_muy_corto_falla():
    with pytest.raises(ValidationError):
        TransactionsDTO(evento_id="EVT-001", item="ab", ingreso=10.0)


@pytest.mark.unit
def test_transacciones_dto_item_muy_largo_falla():
    with pytest.raises(ValidationError):
        TransactionsDTO(evento_id="EVT-001", item="a" * 51, ingreso=10.0)


# ---------------------------------------------------------------------------
# DashboardSummaryResponseDTO
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_dashboard_summary_dto_valido():
    dto = DashboardSummaryResponseDTO(
        total_sales=150.5,
        total_drinks_sold=12,
        active_time="01:30:15",
    )
    assert dto.total_sales == 150.5
    assert dto.total_drinks_sold == 12
    assert dto.active_time == "01:30:15"


@pytest.mark.unit
def test_dashboard_summary_dto_requiere_todos_los_campos():
    with pytest.raises(ValidationError):
        DashboardSummaryResponseDTO(total_sales=150.5, total_drinks_sold=12)


@pytest.mark.unit
def test_dashboard_summary_dto_tipo_invalido_en_active_time():
    with pytest.raises(ValidationError):
        DashboardSummaryResponseDTO(
            total_sales=150.5,
            total_drinks_sold=12,
            active_time=12345,  # debe ser str, no int
        )


# ---------------------------------------------------------------------------
# EventosResponseDTO
# ---------------------------------------------------------------------------


def _datos_evento_response_validos():
    return {
        "cobot_id": "cobot-A",
        "fecha": datetime(2026, 9, 6, 2, 57, 28, tzinfo=timezone.utc),
        "evento_id": "EVT-001",
        "tipo_evento": "InfoRobot",
        "descripcion": "Robot inició ciclo de preparación",
    }


@pytest.mark.unit
def test_eventos_response_dto_valido():
    dto = EventosResponseDTO(**_datos_evento_response_validos())

    assert dto.cobot_id == "cobot-A"
    assert dto.evento_id == "EVT-001"
    assert dto.descripcion == "Robot inició ciclo de preparación"
    assert dto.tipo_evento == TipoEvento.INFO_ROBOT


@pytest.mark.unit
def test_eventos_response_dto_acepta_tipo_evento_como_enum():
    data = _datos_evento_response_validos()
    data["tipo_evento"] = TipoEvento.WARNING
    dto = EventosResponseDTO(**data)
    assert dto.tipo_evento == TipoEvento.WARNING


@pytest.mark.unit
def test_eventos_response_dto_tipo_evento_invalido():
    data = _datos_evento_response_validos()
    data["tipo_evento"] = "TipoInexistente"

    with pytest.raises(ValidationError):
        EventosResponseDTO(**data)


@pytest.mark.unit
@pytest.mark.parametrize(
    "campo_faltante",
    ["cobot_id", "fecha", "evento_id", "tipo_evento", "descripcion"],
)
def test_eventos_response_dto_requiere_todos_los_campos(campo_faltante):
    data = _datos_evento_response_validos()
    del data[campo_faltante]

    with pytest.raises(ValidationError):
        EventosResponseDTO(**data)


@pytest.mark.unit
def test_eventos_response_dto_fecha_con_formato_invalido_falla():
    data = _datos_evento_response_validos()
    data["fecha"] = "no-es-una-fecha"

    with pytest.raises(ValidationError):
        EventosResponseDTO(**data)


@pytest.mark.unit
def test_eventos_response_dto_serializa_tipo_evento_como_string_plano():
    dto = EventosResponseDTO(**_datos_evento_response_validos())

    data_dict = dto.model_dump()
    assert data_dict["tipo_evento"] == "InfoRobot"
    assert isinstance(data_dict["tipo_evento"], str)


@pytest.mark.unit
@pytest.mark.parametrize("tipo", list(TipoEvento))
def test_eventos_response_dto_acepta_todos_los_valores_del_enum(tipo):
    data = _datos_evento_response_validos()
    data["tipo_evento"] = tipo.value
    dto = EventosResponseDTO(**data)
    assert dto.tipo_evento == tipo