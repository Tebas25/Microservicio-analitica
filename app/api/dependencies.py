from fastapi import Depends
from app.db.session import get_databse
from app.repositories.transacciones_repo import TransactionsRepository
from app.services.transaccion_service import TransactionsService
from app.repositories.eventos_repo import EventRepository
from app.services.evento_service import EventService
from app.services.analytics_service import AnalyticsService


def get_transaction_service(db=Depends(get_databse)):
    collection = db.get_collection("transacciones")
    repo = TransactionsRepository(collection)
    service = TransactionsService(repo)
    return service


def get_events_service(db=Depends(get_databse)):
    collection = db.get_collection("eventos")
    repo = EventRepository(collection)
    service = EventService(repo)
    return service


def get_analytics_service(db=Depends(get_databse)):
    transaction_collection = db.get_collection("transacciones")
    events_collection = db.get_collection("eventos")
    transaction_repo = TransactionsRepository(transaction_collection)
    events_repo = EventRepository(events_collection)
    service = AnalyticsService(events_repo, transaction_repo)
    return service
