from sqlalchemy import String, ForeignKey
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    author_id: Mapped[int | None] = mapped_column(ForeignKey("author.id", ondelete="SET NULL"))
    author: Mapped["Author"] = relationship(back_populates="books")

