from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import client
from app.api.v1.routers import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await client.close()


app = FastAPI(
    title="API Bartender Robótico - Microservicio Analítica",
    description="Estructura base de la API local.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_v1_router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Estructura base configurada y en línea."}
