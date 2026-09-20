from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class DictionaryEntry(Base):
    __tablename__ = "dictionary_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String)
    search_key: Mapped[str] = mapped_column(String)
    reading: Mapped[str] = mapped_column(String)
    entry: Mapped[str] = mapped_column(String)
