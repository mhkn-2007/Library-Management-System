from sqlalchemy import select
from sqlalchemy.orm import Session, and_
from app.models import Book
from app.schemas.book_schema import BookCreate, BookUpdate


def add_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int) -> Book:
    return db.execute(select(Book).where(Book.id == book_id)).one_or_none()


def get_books(db: Session, last_id: int | None = None, limit: int = 10) -> list[Book]:
    books = []
    if last_id:
        result = db.execute(
            select(Book).where(Book.id > last_id).order_by(Book.id.asc()).limit(limit)
        )
        books = result.scalars().all()
    else:
        result = db.execute(select(Book).order_by(Book.id.asc()).limit(limit))
        books = result.scalars().all()
    next_last_id = books[-1].id if books else None
    return {"items": books, "next_last_id": next_last_id}


def update_book(db: Session, book: BookUpdate) -> Book:
    db_book = db.execute(select(Book).where(Book.id == book.id)).scalar_one_or_none()
    if not db_book:
        return None
    for field, value in book.dict(exclude_unset=True).items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = db.execute(select(Book).where(Book.id == book_id)).scalar_one_or_none()
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True


def exists_book(db: Session, book: BookCreate) -> bool:
    return (
        db.execute(
            select(Book).where(
                and_(
                    Book.title == book.title,
                    Book.author == book.author,
                    Book.publish_year == book.publish_year,
                )
            )
        ).scalar_one_or_none()
        is not None
    )
