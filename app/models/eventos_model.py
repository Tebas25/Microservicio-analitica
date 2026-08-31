from typing import Annotated, Optional
from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from datetime import datetime, timezone

PyObjectId = Annotated[
    str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)
]


class EventosEntity(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    fecha: datetime = Field(default_factory=datetime.now(timezone.utc))
    tipo_evento: str
    descripcion: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
