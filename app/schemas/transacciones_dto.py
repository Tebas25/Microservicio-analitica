from pydantic import BaseModel, Field


class TransactionsDTO(BaseModel):
    evento_id: str
    cobot_id: str
    item: str = Field(min_length=3, max_length=50)
    ingreso: float = Field(ge=0)


class RankingDrinkDTO(BaseModel):
    drink: str
    number: int
