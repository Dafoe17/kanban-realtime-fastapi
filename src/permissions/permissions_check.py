def check_board_permission(
    db,
    user,
    board_id,
    permission,
):

    from fastapi import HTTPException

    from src.permissions import ROLE_PERMISSIONS, Permission
    from src.repositories import UsersRepository

    user_in_board = UsersRepository.get_user_in_board(
        db, user_id=user.id, board_id=board_id
    )
    if not user_in_board:
        raise HTTPException(status_code=403, detail="Not member")

    base_rules = ROLE_PERMISSIONS[user_in_board.role]
    custom_rules = {Permission(p) for p in user_in_board.custom_permissions}
    all_rules = {*base_rules, *custom_rules}

    if permission not in all_rules:
        raise HTTPException(status_code=403, detail="Access denied")
