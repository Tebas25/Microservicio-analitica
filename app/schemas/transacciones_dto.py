from pydantic import BaseModel, Field


class TransaccionesDTO(BaseModel):
    item: str = Field(min_length=3, max_length=50)
    ingreso: float = Field(ge=0)
