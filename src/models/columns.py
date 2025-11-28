from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from src.database import Base
from datetime import datetime
import uuid

class Column(Base):
    __tablename__ = 'columns'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, 
                                          default=lambda: str(uuid.uuid4()), 
                                          nullable=False, index=True)
    board_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), 
                                                ForeignKey("boards.id", ondelete="CASCADE"), 
                                                nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
