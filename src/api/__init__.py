from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.boards import router as boards_router
from src.api.cards import router as cards_router
from src.api.columns import router as columns_router
from src.api.invites import router as invites_router
from src.api.user_board_preferences import router as user_board_prefs_router
from src.api.users import router as users_router
from src.database import Base, engine
from src.ws.endpoints import router as ws_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(users_router)
main_router.include_router(boards_router)
main_router.include_router(user_board_prefs_router)
main_router.include_router(columns_router)
main_router.include_router(cards_router)
main_router.include_router(invites_router)
main_router.include_router(ws_router)

Base.metadata.create_all(bind=engine)
