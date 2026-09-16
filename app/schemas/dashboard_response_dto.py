from pydantic import BaseModel


class DashboardSummaryResponseDTO(BaseModel):
    total_sales: float
    total_drinks_sold: int
    active_time: str
