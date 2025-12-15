from uuid import UUID

from fastapi import HTTPException

from src.permissions import Permission, check_board_permission
from src.repositories import (
    BoardsRepository,
    CardsRepository,
    ColumnsRepository,
    CommentsRepository,
)
from src.schemas import CommentCreate, CommentRead, CommentUpdate
from src.ws import CommentCreatedPayload, CommentDeletedPayload, CommentUpdatedPayload


class CommentsService:

    @staticmethod
    def get_comment(db, comment_id: UUID, current_user) -> CommentRead:
        comment = CommentsRepository.get_comment(db, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        card = CardsRepository.get_card(db, comment.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_VIEW)

        return CommentRead.model_validate(comment)

    @staticmethod
    def create_comment(
        card_id: UUID, db, current_user, data: CommentCreate
    ) -> CommentCreatedPayload:
        card = CardsRepository.get_card(db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        try:
            db_comment = CommentsRepository.add_comment(
                db, data, card_id, current_user.id
            )
            payload = CommentCreatedPayload.model_validate(
                {**db_comment.__dict__, "card_id": card_id, "board_id": board.id}
            )
            return payload
        except Exception as e:
            CommentsRepository.rollback(db)
            raise HTTPException(500, f"Failed to create comment: {str(e)}")

    @staticmethod
    def update_comment(
        comment_id: UUID, db, current_user, data: CommentUpdate
    ) -> CommentUpdatedPayload:

        comment = CommentsRepository.get_comment(db, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        card = CardsRepository.get_card(db, comment.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        if comment.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        comment_dict = data.model_dump()
        try:
            db_comment = CommentsRepository.patch_comment(db, comment_dict, comment)
            payload = CommentUpdatedPayload.model_validate(
                {
                    **db_comment.__dict__,
                    "card_id": comment.card_id,
                    "board_id": board.id,
                }
            )
            return payload
        except Exception as e:
            CommentsRepository.rollback(db)
            raise HTTPException(500, f"Failed to update comment: {str(e)}")

    @staticmethod
    def delete_comment(comment_id: UUID, db, current_user) -> CommentDeletedPayload:

        comment = CommentsRepository.get_comment(db, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        card = CardsRepository.get_card(db, comment.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        if comment.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        try:
            db_comment = CommentsRepository.delete_comment(db, comment)
            payload = CommentDeletedPayload.model_validate(
                {
                    **db_comment.__dict__,
                    "card_id": comment.card_id,
                    "board_id": board.id,
                }
            )
            return payload
        except Exception as e:
            CommentsRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete comment: {str(e)}")
