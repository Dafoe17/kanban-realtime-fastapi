from uuid import UUID

from fastapi import HTTPException

from src.permissions import Permission, check_board_permission
from src.repositories import BoardsRepository, ColumnsRepository
from src.schemas import (
    ColumnCreate,
    ColumnMove,
    ColumnRead,
    ColumnsListResponse,
    ColumnUpdate,
)
from src.ws import (
    ColumnCreatedPayload,
    ColumnDeletedPayload,
    ColumnMovedPayload,
    ColumnUpdatedPayload,
)


class ColumnsService:

    @staticmethod
    def get_column(db, column_id: UUID, current_user) -> ColumnRead:
        column = ColumnsRepository.get_column(db, column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_VIEW)

        return ColumnRead.model_validate(column)

    @staticmethod
    def get_board_columns(
        db, board_id: UUID, current_user, skip: int | None
    ) -> ColumnsListResponse:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_VIEW)

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
    def create_column(
        db, board_id: UUID, current_user, data: ColumnCreate
    ) -> ColumnCreatedPayload:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        db_columns = ColumnsRepository.get_last_board_column(db, board_id)
        new_position = db_columns[0] + 1 if db_columns else 0

        try:
            db_column = ColumnsRepository.add_column(db, data, board_id, new_position)
            payload = ColumnCreatedPayload.model_validate(db_column)
            return payload
        except Exception as e:
            ColumnsRepository.rollback(db)
            raise HTTPException(500, f"Failed to create board: {str(e)}")

    @staticmethod
    def delete_column(db, column_id: UUID, current_user) -> ColumnDeletedPayload:
        column = ColumnsRepository.get_column(db, column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        try:
            db_column = ColumnsRepository.delete_column(db, column)
            payload = ColumnDeletedPayload.model_validate(db_column)
            return payload
        except Exception as e:
            ColumnsRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete column: {str(e)}")

    @staticmethod
    def patch_column(
        db, column_id: UUID, current_user, data: ColumnUpdate
    ) -> ColumnUpdatedPayload:
        column = ColumnsRepository.get_column(db, column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        column_dict = data.model_dump()
        try:
            db_column = ColumnsRepository.patch_column(db, column, column_dict)
            payload = ColumnUpdatedPayload.model_validate(db_column)
            return payload
        except Exception as e:
            ColumnsRepository.rollback(db)
            raise HTTPException(500, f"Failed to patch column: {str(e)}")

    @staticmethod
    def move_column(
        db, column_id: UUID, current_user, data: ColumnMove
    ) -> ColumnMovedPayload:
        column = ColumnsRepository.get_column(db, column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        db_columns = list(ColumnsRepository.get_board_columns(db, board.id))
        if data.position < 0 or data.position >= db_columns[-1].position:
            raise HTTPException(
                400, f"Failed to move, invalid position: {data.position}"
            )

        old_position = column.position
        new_position = data.position

        if old_position == new_position:
            return ColumnMovedPayload.model_validate(column)

        try:
            db_column = ColumnsRepository.move_column(
                db, board.id, column, new_position, old_position
            )
            payload = ColumnMovedPayload.model_validate(db_column)
            return payload
        except Exception as e:
            ColumnsRepository.rollback(db)
            raise HTTPException(500, f"Failed to move column: {str(e)}")
