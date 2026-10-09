from sqlalchemy import Integer , String
from sqlalchemy.orm import Mapped,mapped_column
from database.database import Base

class Book(Base):
    __tablename__="books"

    id : Mapped[int] = mapped_column(...,Integer , primary_key=True , index= True)

    title : Mapped[str] = mapped_column(...,String(50))
    author_name : Mapped[str] = mapped_column(...,String(50))
    publish_year : Mapped[str] = mapped_column(...,Integer(4))

    