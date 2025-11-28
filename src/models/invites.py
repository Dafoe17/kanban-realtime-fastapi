from sqlalchemy import String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from src.database import Base
import uuid

class Invite(Base):
    __tablename__ = 'invites'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, 
                                          default=lambda: str(uuid.uuid4()), 
                                          nullable=False, index=True)
    board_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"), 
                                                nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"), 
                                                nullable=False, index=True)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expiret_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now() + timedelta(hours=1))
