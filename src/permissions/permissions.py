from .roles import Permission, Role

ROLE_PERMISSIONS = {
    Role.guest: {Permission.BOARD_VIEW, Permission.COLUMN_VIEW, Permission.CARD_VIEW},
    Role.user: {
        Permission.BOARD_VIEW,
        Permission.COLUMN_VIEW,
        Permission.CARD_VIEW,
        Permission.CARD_CREATE,
        Permission.CARD_UPDATE,
        Permission.CARD_MOVE,
    },
    Role.manager: {
        Permission.BOARD_VIEW,
        Permission.BOARD_INVITE,
        Permission.COLUMN_VIEW,
        Permission.COLUMN_CREATE,
        Permission.COLUMN_UPDATE,
        Permission.COLUMN_DELETE,
        Permission.CARD_VIEW,
        Permission.CARD_CREATE,
        Permission.CARD_UPDATE,
        Permission.CARD_DELETE,
        Permission.CARD_MOVE,
        Permission.USER_REMOVE,
    },
    Role.admin: set(item for item in Permission),
}
