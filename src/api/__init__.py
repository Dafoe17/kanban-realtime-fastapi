from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.boards import router as boards_router
from src.api.users import router as users_router
from src.database import Base, engine

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(users_router)
main_router.include_router(boards_router)

Base.metadata.create_all(bind=engine)
