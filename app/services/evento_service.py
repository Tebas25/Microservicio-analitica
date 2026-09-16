from app.repositories.eventos_repo import EventRepository
from app.schemas.eventos_dto import EventsDTO
from app.models.eventos_model import EventsEntity


class EventService:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    async def create_event(self, event_dto: EventsDTO):
        events = EventsEntity(**event_dto.model_dump())
        events_dict = events.model_dump(by_alias=True, exclude_none=True)
        return await self.event_repository.create_event(events_dict)
