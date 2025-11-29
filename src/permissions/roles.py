from enum import Enum


class Role(str, Enum):
    guest = "guest"
    user = "user"
    manager = "manager"
    admin = "admin"


class Permission(str, Enum):
    BOARD_VIEW = "board:view"
    BOARD_UPDATE = "board:update"
    BOARD_DELETE = "board:delete"
    BOARD_INVITE = "board:invite"

    COLUMN_VIEW = "column:view"
    COLUMN_CREATE = "column:create"
    COLUMN_UPDATE = "column:update"
    COLUMN_DELETE = "column:delete"

    CARD_VIEW = "column:view"
    CARD_CREATE = "card:create"
    CARD_UPDATE = "card:update"
    CARD_DELETE = "card:delete"
    CARD_MOVE = "card:move"

    USER_REMOVE = "user:remove"
    USER_CHANGE_ROLE = "user:change_role"
