from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Card(Base):
    __tablename__ = 'cards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    column_id: Mapped[int] = mapped_column(Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    assigned_to: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
