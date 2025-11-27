from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.database import Base
from src.enums import UserRole

class Member(Base):
    __tablename__ = 'members'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    board_id: Mapped[int] = mapped_column(Integer, ForeignKey("board.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default="quest")
    added_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
