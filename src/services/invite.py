from uuid import UUID

from fastapi import HTTPException

from src.permissions import Permission, Role, check_board_permission
from src.repositories import BoardsRepository, InviteRepository, UserBoardPrefRepository
from src.schemas import InviteRead, UserBoardPreferencesCreate, UserBoardPreferencesRead


class InviteService:

    @staticmethod
    def create_invite(
        board_id: UUID, db, current_user, max_uses: int | None
    ) -> InviteRead:

        board = BoardsRepository.get_board(db, id=board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_INVITE_LINK)

        if not max_uses:
            max_uses = 1

        try:
            invite = InviteRepository.create_invite(
                db, board_id, current_user.id, max_uses
            )
            return InviteRead.model_validate(invite)
        except Exception as e:
            InviteRepository.rollback(db)
            raise HTTPException(500, f"Failed to create invite: {str(e)}")

    @staticmethod
    def use_invite(invite_id: UUID, db, current_user) -> UserBoardPreferencesRead:

        invite = InviteRepository.get_invite(db, invite_id)
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found or expired")

        board = BoardsRepository.get_board(db, id=invite.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        if UserBoardPrefRepository.check_is_member(db, board.id, current_user.id):
            raise HTTPException(status_code=409, detail="User already board member")

        try:
            invite = InviteRepository.use_invite(db, invite)
            db_prefs = BoardsRepository.get_last_board_pref(db, current_user.id)
            new_position = db_prefs[0] + 1 if db_prefs else 0
            prefs = UserBoardPreferencesCreate(
                board_id=board.id,
                user_id=current_user.id,
                role=Role.user,
                position=new_position,
                custom_title=board.title,
            )
            prefs = BoardsRepository.add_preferences(db, prefs)
            return UserBoardPreferencesRead.model_validate(prefs)
        except Exception as e:
            InviteRepository.rollback(db)
            raise HTTPException(500, f"Failed to use invite: {str(e)}")

    @staticmethod
    def get_invite_info(invite_id: UUID, db, current_user) -> InviteRead:

        invite = InviteRepository.get_invite(db, invite_id)
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found or expired")

        board = BoardsRepository.get_board(db, id=invite.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_INVITE_LINK)

        return InviteRead.model_validate(invite)

    @staticmethod
    def delete_invite(invite_id: UUID, db, current_user) -> InviteRead:
        invite = InviteRepository.get_invite(db, invite_id)
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found or expired")

        board = BoardsRepository.get_board(db, id=invite.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_INVITE_LINK)

        try:
            db_invite = InviteRepository.delete_invite(db, invite)
            return InviteRead.model_validate(db_invite)
        except Exception as e:
            InviteRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete invite: {str(e)}")
