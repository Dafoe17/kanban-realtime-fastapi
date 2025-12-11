from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class CardTagAssociation(Base):
    __tablename__ = "card_tag_association"

    card_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cards.id"),
        nullable=False,
        index=True)
    
    tag_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tags.id"),
        nullable=False,
        index=True)
    
    __table_args__ = (
        UniqueConstraint("tag_id", "card_id", name="uq_tags_for_card"),
    )
