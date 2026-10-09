from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., max_length=50, min_length=1)
    author_name: str = Field(..., max_length=50, min_length=1)
    publish_year: int = Field(..., le=datetime.now().year, ge=1450)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(None, max_length=50, min_length=1)
    author_name: str | None = Field(None, max_length=50, min_length=1)
    publish_year: int | None = Field(None, le=datetime.now().year, ge=1450)


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookPage(BaseModel):
    items: list[BookRead]
    next_last_id: int | None
