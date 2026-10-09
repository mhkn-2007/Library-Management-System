from pydantic import BaseModel, field_validator , Field
from time import datetime


class BookBase(BaseModel):
    title: str = Field(..., max_length=50, min_length=1)
    author: str = Field(..., max_length=50, min_length=1)
    publish_year: int = Field(..., le=datetime.now().year, ge=1450)

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    id: int = Field(..., gt=0)

