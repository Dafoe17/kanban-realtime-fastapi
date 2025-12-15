from uuid import uuid4

from src.schemas import BoardCreate

from .prefixes import BOARD_PREFIX


def generate_test_board(board_prefix=BOARD_PREFIX):
    return BoardCreate(title=f"{board_prefix}_{uuid4().hex[:6]}")
