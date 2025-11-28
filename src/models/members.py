from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.database import Base
from src.enums import UserRole
import uuid

class Member(Base):
    __tablename__ = 'members'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, 
                                          default=lambda: str(uuid.uuid4()), 
                                          nullable=False, index=True)
    board_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), 
                                                ForeignKey("boards.id", ondelete="CASCADE"),
                                                nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), 
                                               ForeignKey("users.id", ondelete="CASCADE"), 
                                               nullable=False, index=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default="quest")
    added_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
