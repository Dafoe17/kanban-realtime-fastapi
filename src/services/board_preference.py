from uuid import UUID

from fastapi import HTTPException

from src.repositories import UserBoardPrefRepository
from src.schemas import (
    UserBoardPreferencesBooalenUpdate,
    UserBoardPreferencesListResponse,
    UserBoardPreferencesRead,
    UserBoardPreferencesUpdate,
)


class BoardPreferencesService:

    @staticmethod
    def get_my_board_preferences(db, current_user) -> UserBoardPreferencesListResponse:
        board_prefs = UserBoardPrefRepository.get_user_boards(db, current_user.id)
        total = UserBoardPrefRepository.count(board_prefs)

        response = UserBoardPreferencesListResponse(
            total=total,
            skip=None,
            limit=None,
            boards=[
                UserBoardPreferencesRead.model_validate(board_pref)
                for board_pref in board_prefs
            ],
        )

        return response

    @staticmethod
    def get_board_preference_by_id(
        db, current_user, pref_id: UUID
    ) -> UserBoardPreferencesRead:
        board_pref = UserBoardPrefRepository.get_pref_by_id(db, pref_id)

        if not board_pref:
            raise HTTPException(
                status_code=404, detail="User preferences for the board not found"
            )

        return UserBoardPreferencesRead.model_validate(board_pref)

    @staticmethod
    def patch_user_board_preference(
        db, current_user, data: UserBoardPreferencesUpdate, pref_id: UUID
    ) -> UserBoardPreferencesRead:
        board_pref = UserBoardPrefRepository.get_pref_by_id(db, pref_id)

        if not board_pref:
            raise HTTPException(
                status_code=404, detail="User preferences for the board not found"
            )

        pref_dict = data.model_dump()

        try:
            db_pref = UserBoardPrefRepository.patch_pref(db, board_pref, pref_dict)
            return UserBoardPreferencesRead.model_validate(db_pref)
        except Exception as e:
            UserBoardPrefRepository.rollback(db)
            raise HTTPException(
                500, f"Failed to change user preferences for board: {str(e)}"
            )

    @staticmethod
    def patch_user_board_state(
        db, current_user, pref_id: UUID, data: UserBoardPreferencesBooalenUpdate
    ) -> UserBoardPreferencesRead:
        board_pref = UserBoardPrefRepository.get_pref_by_id(db, pref_id)

        if not board_pref:
            raise HTTPException(
                status_code=404, detail="User preferences for the board not found"
            )

        pref_dict = data.model_dump()

        try:
            db_pref = UserBoardPrefRepository.patch_pref(db, board_pref, pref_dict)
            return UserBoardPreferencesRead.model_validate(db_pref)
        except Exception as e:
            UserBoardPrefRepository.rollback(db)
            raise HTTPException(
                500, f"Failed to change user preferences for board: {str(e)}"
            )
