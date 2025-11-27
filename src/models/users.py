from sqlalchemy import Integer, String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.database import Base
from src.enums import UserRole

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default="quest")
    date_joined: Mapped[datetime] = mapped_column(DateTime, nullable=False)
