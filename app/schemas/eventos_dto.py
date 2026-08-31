from pydantic import BaseModel
from enum import Enum


class TipoEvento(str, Enum):
    INFO_ROBOT = "InfoRobot"
    INFO_SISTEMA = "InfoSistema"
    WARNING = "Warning"
    ERROR_ROBOT = "ErrorRobot"
    ERROR_SISTEMA = "ErrorSistema"


class EventosDTO(BaseModel):
    tipo_evento: TipoEvento
    descripcion: str
