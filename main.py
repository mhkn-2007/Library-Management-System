import uvicorn
from fastapi import FastAPI

from app.database.database import Base, engine
from app.routers.book_router import router as book_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="A simple Library Management System built with FastAPI, SQLite, SQLAlchemy, and Pydantic to manage books and perform CRUD operations.",
    version="0.1.0",
)


app.include_router(book_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
