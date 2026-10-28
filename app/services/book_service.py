from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import book_crud
from app.schemas.book_schemas import BookCreate, BookUpdate


async def create_book(db: Session, book: BookCreate):
    if await book_crud.exists_book(db, book):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists"
        )
    return await book_crud.add_book(db, book)


async def get_book(db: Session, book_id: int):
    book = await book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


async def get_books(db: Session, last_id: int | None = None, limit: int = 10):
    return await book_crud.get_books(db, last_id, limit)


async def update_book(db: Session, book_id: int, book: BookUpdate):
    updated_book = await book_crud.update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return updated_book


async def delete_book(db: Session, book_id: int):
    success = await book_crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
