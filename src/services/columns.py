from uuid import UUID

from fastapi import HTTPException

from src.permissions import Permission, check_board_permission
from src.repositories import BoardsRepository, ColumnsRepository
from src.schemas import ColumnCreate, ColumnRead, ColumnsListResponse, ColumnUpdate


class ColumnsService:

    @staticmethod
    def get_column(db, column_id: UUID, current_user) -> ColumnRead:
        column = ColumnsRepository.get_column(db, column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.COLUMN_VIEW)

        return ColumnRead.model_validate(column)

    @staticmethod
    def get_board_columns(
        db, board_id: UUID, current_user, skip: int | None
    ) -> ColumnsListResponse:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.COLUMN_VIEW)

        query = ColumnsRepository.get_board_columns(db, board_id)
        total = ColumnsRepository.count(query)
        columns = ColumnsRepository.paginate(query, skip, 5)

        response = ColumnsListResponse(
            total=total,
            skip=skip,
            limit=5,
            columns=[ColumnRead.model_validate(column) for column in columns],
        )

        return response

    @staticmethod
    def create_column(db, board_id: UUID, current_user, data: ColumnCreate):
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.COLUMN_CREATE)

        try:
            column = ColumnsRepository.add_column(db, data, board_id)
            # to do
            # prefs = UserColumnPreferencesCreate
            return ColumnRead.model_validate(column)
        except Exception as e:
            ColumnsRepository.rollback(db)
            raise HTTPException(500, f"Failed to create board: {str(e)}")

    @staticmethod
    def delete_column(db, column_id: UUID, current_user):
        column = ColumnsRepository.get_column(db, column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.COLUMN_DELETE)

        try:
            db_column = ColumnsRepository.delete_column(db, column)
            return ColumnRead.model_validate(db_column)
        except Exception as e:
            ColumnsRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete column: {str(e)}")

    @staticmethod
    def patch_column(
        db, column_id: UUID, current_user, data: ColumnUpdate
    ) -> ColumnRead:
        column = ColumnsRepository.get_column(db, column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.COLUMN_UPDATE)

        column_dict = data.model_dump()
        try:
            db_column = ColumnsRepository.patch_column(db, column, column_dict)
            return ColumnRead.model_validate(db_column)
        except Exception as e:
            ColumnsRepository.rollback(db)
            raise HTTPException(500, f"Failed to patch column: {str(e)}")
