from enum import Enum


class Role(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"


class Permission(str, Enum):
    BOARD_VIEW = "board:view"
    BOARD_WRITE = "board:write"
    BOARD_MANAGE = "board:manage"
    BOARD_INVITE_LINK = "board:invite_link"
    CARD_MOVE = "card:move"
    CARD_UPDATE_STATUS = "card:update_status"
    USER_MANAGE = "user:manage"
