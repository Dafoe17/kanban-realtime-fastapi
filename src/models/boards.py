from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Board(Base):
    __tablename__ = 'boards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    owned_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
