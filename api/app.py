from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.enums_controllers import router as enums_router
from controllers.filmes_controllers import router as filmes_router
from database import database


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    await database.connect()
    try:
        yield
    finally:
        await database.disconnect()


app = FastAPI(title="Cinelist API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://zenvexy.github.io",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)


@app.get("/", tags=["Status"])
async def inicio():
    return {
        "mensagem": "CineList API online",
        "documentacao": "/docs",
    }


app.include_router(filmes_router, prefix="/api")
app.include_router(enums_router, prefix="/api")
