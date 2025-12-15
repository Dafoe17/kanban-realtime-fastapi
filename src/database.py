from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker  # noqa: F401

from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)

Session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

from src.models import (  # noqa: E402,F401
    Board,
    Card,
    CardTagAssociation,
    Checklist,
    ChecklistItem,
    Column,
    Comment,
    Invite,
    Tag,
    User,
    UserBoardPreference,
)
