from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.database.database import Base, engine
from app.routers.book_router import router as book_router

from app.models import Book


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    title="Library Management System",
    description=(
        "A simple Library Management System built with FastAPI, "
        "PostgreSQL, SQLAlchemy, and Pydantic to manage books "
        "and perform CRUD operations."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(book_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
