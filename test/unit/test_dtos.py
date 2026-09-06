import pytest
from pydantic import ValidationError

from app.schemas.eventos_dto import EventsDTO, TipoEvento
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
