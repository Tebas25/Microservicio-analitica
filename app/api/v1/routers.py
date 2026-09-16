from fastapi import APIRouter
from app.api.v1 import endpoint

router = APIRouter(prefix="/api/v1/analytics")
router.include_router(endpoint.router)
