from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Column(Base):
    __tablename__ = 'columns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    board_id: Mapped[int] = mapped_column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
