from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from pgvector.sqlalchemy import VECTOR

Base = declarative_base()

class Document(Base):
    """
    SQLAlchemy ORM model for a document chunk.
    """
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column()
    embedding: Mapped[VECTOR] = mapped_column(VECTOR(1024))
    source: Mapped[str] = mapped_column(index=True) 