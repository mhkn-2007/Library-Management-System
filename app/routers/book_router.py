from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.book_schemas import BookCreate, BookPage, BookRead, BookUpdate
from app.services import book_service

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=BookPage)
async def get_books(
    db: Session = Depends(get_db), last_id: int | None = None, limit: int = 10
):
    return await book_service.get_books(db, last_id, limit)


@router.get("/{book_id}", response_model=BookRead)
async def get_book(
    book_id: int = Path(..., gt=0, title="Book ID", description="Enter The Book Id"),
    db: Session = Depends(get_db),
):
    return await book_service.get_book(db, book_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BookRead)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return await book_service.create_book(db, book)


@router.patch("/{book_id}", response_model=BookRead)
async def update_book(
    book: BookUpdate,
    book_id: int = Path(..., gt=0, title="Book ID", description="Enter The Book Id"),
    db: Session = Depends(get_db),
):
    return await book_service.update_book(db, book_id, book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int = Path(..., gt=0, title="Book ID", description="Enter The Book Id"),
    db: Session = Depends(get_db),
):
    await book_service.delete_book(db, book_id)
