from .roles import Permission, Role

ROLE_PERMISSIONS = {
    Role.user: {
        Permission.BOARD_VIEW,
        Permission.CARD_MOVE,
        Permission.CARD_UPDATE_STATUS,
    },
    Role.manager: {
        Permission.BOARD_VIEW,
        Permission.BOARD_WRITE,
        Permission.BOARD_MANAGE,
        Permission.CARD_MOVE,
        Permission.CARD_UPDATE_STATUS,
    },
    Role.admin: set(item for item in Permission),
}
