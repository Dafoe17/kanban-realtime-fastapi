import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database import Base
from src.models import Attachment, Checklist, Comment, Tag


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4(),
        nullable=False,
        index=True,
    )
    column_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("columns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assigned_to: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    attachment: Mapped[list[Attachment]] = relationship(
        "Attachment", cascade="all, delete"
    )
    checklist: Mapped[list[Checklist]] = relationship(
        "Checklist", cascade="all, delete"
    )
    comment: Mapped[list[Comment]] = relationship("Comment", cascade="all, delete")
    tag: Mapped[list[Tag]] = relationship("Tag", cascade="all, delete")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("column_id", "position", name="uq_card_position"),
    )
