import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UserColumnPreference(Base):
    __tablename__ = "user_column_preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
        index=True,
    )
    column_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("columns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    custom_title: Mapped[str] = mapped_column(String, nullable=True)
    color: Mapped[str] = mapped_column(String, nullable=False)
    notification_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, index=True
    )
    is_pinned: Mapped[bool] = mapped_column(Boolean, nullable=False, index=True)
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False, index=True)
    added_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
