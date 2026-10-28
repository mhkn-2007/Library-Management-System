from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Book
from app.schemas.book_schemas import BookCreate, BookUpdate


async def add_book(db: AsyncSession, book: BookCreate) -> Book:
    db_book = Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def get_book(db: AsyncSession, book_id: int) -> Book | None:
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def get_books(
    db: AsyncSession, last_id: int | None = None, limit: int = 10
) -> dict:
    query = select(Book).order_by(Book.id.asc()).limit(limit)

    if last_id is not None:
        query = query.where(Book.id > last_id)

    result = await db.execute(query)
    books = result.scalars().all()
    next_last_id = books[-1].id if books else None

    return {"items": books, "next_last_id": next_last_id}


async def update_book(db: AsyncSession, book_id: int, book: BookUpdate) -> Book | None:
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar_one_or_none()

    if db_book is None:
        return None

    for field, value in book.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(db_book, field, value)

    await db.commit()
    await db.refresh(db_book)
    return db_book


async def delete_book(db: AsyncSession, book_id: int) -> bool:
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar_one_or_none()

    if db_book is None:
        return False

    await db.delete(db_book)
    await db.commit()
    return True


async def exists_book(db: AsyncSession, book: BookCreate) -> bool:
    result = await db.execute(
        select(Book).where(
            and_(
                Book.title == book.title,
                Book.author_name == book.author_name,
                Book.publish_year == book.publish_year,
            )
        )
    )

    return result.scalar_one_or_none() is not None
