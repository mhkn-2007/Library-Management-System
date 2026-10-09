from app.models import Book
from app.schemas.book_schema import BookCreate, BookUpdate  
from app.crud import book_crud
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

async def create_book(db: Session, book: BookCreate):
    if book_crud.exists_book(db, book):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")
    return book_crud.add_book(db, book)

async def get_book(db: Session, book_id: int):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

async def get_books(db: Session, last_id: int | None = None, limit: int = 10):
    return book_crud.get_books(db, last_id, limit) 

async def update_book(db: Session, book: BookUpdate):
    updated_book = book_crud.update_book(db, book)
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return updated_book

async def delete_book(db: Session, book_id: int):
    success = book_crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {"message": "Book deleted successfully"} 