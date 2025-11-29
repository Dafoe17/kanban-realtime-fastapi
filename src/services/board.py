from uuid import UUID

from fastapi import HTTPException

from src.permissions import Permission, Role
from src.repositories import BoardsRepository
from src.schemas import (
    BoardCreate,
    BoardRead,
    BoardsListResponse,
    BoardUpdate,
    UserBoardPreferencesRead,
)


class BoardsService:

    @staticmethod
    def get_board(db, id: UUID, current_user) -> BoardRead:

        board = BoardsRepository.get_board(db, id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        return BoardRead.model_validate(board)

    @staticmethod
    def get_my_boards(db, current_user, skip) -> BoardsListResponse:
        query = BoardsRepository.get_user_boards(db, current_user.id)
        total = BoardsRepository.count(query)
        boards = BoardsRepository.paginate(query, skip, 5)

        response = BoardsListResponse(
            total=total,
            skip=skip,
            limit=5,
            boards=[BoardRead.model_validate(board) for board in boards],
        )

        return response

    @staticmethod
    def create_board(db, data: BoardCreate, current_user) -> BoardRead:

        data = data.model_copy(update={"owner_id": current_user.id})
        try:
            board = BoardsRepository.add_board(db, data)
            return BoardRead.model_validate(board)
        except Exception as e:
            BoardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to create board: {str(e)}")

    @staticmethod
    def delete_board(db, id: UUID) -> BoardRead:

        board = BoardsRepository.get_board(db, id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        try:
            board = BoardsRepository.delete_board(db, board)
            return BoardRead.model_validate(board)
        except Exception as e:
            BoardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete board: {str(e)}")

    @staticmethod
    def patch_board(db, data: BoardUpdate, board_id: UUID) -> BoardRead:

        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        board_dict = data.model_dump()
        try:
            board = BoardsRepository.patch_board(db, board, board_dict)
            return BoardRead.model_validate(board)
        except Exception as e:
            BoardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete board: {str(e)}")

    @staticmethod
    def change_role_or_permissions(
        db,
        user_id: UUID,
        board_id: UUID,
        role: Role | None,
        custom_permissions: list[Permission] | None,
    ) -> UserBoardPreferencesRead:

        user_in_board = BoardsRepository.is_user_in_board(db, board_id, user_id)
        if not user_in_board:
            raise HTTPException(status_code=404, detail="User in board not found")

        try:
            user_in_board = BoardsRepository.patch_role_or_permissions(
                db, user_in_board, role, custom_permissions
            )
            return UserBoardPreferencesRead.model_validate(user_in_board)
        except Exception as e:
            BoardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to create board: {str(e)}")
