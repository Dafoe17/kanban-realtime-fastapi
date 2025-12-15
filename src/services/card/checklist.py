from uuid import UUID

from fastapi import HTTPException

from src.permissions import Permission, check_board_permission
from src.repositories import (
    BoardsRepository,
    CardsRepository,
    ChecklistRepository,
    ColumnsRepository,
)
from src.schemas import (
    ChecklistCreate,
    ChecklistItemCreate,
    ChecklistItemFlag,
    ChecklistItemRead,
    ChecklistItemUpdate,
    ChecklistRead,
    ChecklistUpdate,
)
from src.ws import (
    ChecklistCreatedPayload,
    ChecklistDeletedPayload,
    ChecklistItemCreatedPayload,
    ChecklistItemDeletedPayload,
    ChecklistItemFlagPayload,
    ChecklistItemUpdatedPayload,
    ChecklistUpdatedPayload,
)


class ChecklistsService:

    @staticmethod
    def get_checklist(db, checklist_id: UUID, current_user) -> ChecklistRead:
        checklist = ChecklistRepository.get_checklist(db, checklist_id)
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")

        card = CardsRepository.get_card(db, checklist.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_VIEW)

        return ChecklistRead.model_validate(checklist)

    @staticmethod
    def get_item(db, item_id: UUID, current_user) -> ChecklistItemRead:
        item = ChecklistRepository.get_item(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Checklist item not found")

        checklist = ChecklistRepository.get_checklist(db, item.checklist_id)
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")

        card = CardsRepository.get_card(db, checklist.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_VIEW)

        return ChecklistItemRead.model_validate(item)

    @staticmethod
    def create_checklist(
        db, card_id: UUID, data: ChecklistCreate, current_user
    ) -> ChecklistCreatedPayload:
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
            db_checklist = ChecklistRepository.add_checklist(
                db, data, card_id, current_user.id
            )
            payload = ChecklistCreatedPayload.model_validate(
                {**db_checklist.__dict__, "card_id": card_id, "board_id": board.id}
            )
            return payload
        except Exception as e:
            ChecklistRepository.rollback(db)
            raise HTTPException(500, f"Failed to create checklist: {str(e)}")

    @staticmethod
    def create_item(
        db, checklist_id: UUID, data: ChecklistItemCreate, current_user
    ) -> ChecklistItemCreatedPayload:
        checklist = ChecklistRepository.get_checklist(db, checklist_id)
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")

        card = CardsRepository.get_card(db, checklist.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        if checklist.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        check_board_permission(db, current_user, board.id, Permission.BOARD_VIEW)

        try:
            db_item = ChecklistRepository.add_item(db, data, checklist_id)
            payload = ChecklistItemCreatedPayload.model_validate(
                {**db_item.__dict__, "checklist_id": checklist_id, "board_id": board.id}
            )
            return payload
        except Exception as e:
            ChecklistRepository.rollback(db)
            raise HTTPException(500, f"Failed to create checklist item: {str(e)}")

    @staticmethod
    def update_checklist(
        db, checklist_id: UUID, data: ChecklistUpdate, current_user
    ) -> ChecklistUpdatedPayload:
        checklist = ChecklistRepository.get_checklist(db, checklist_id)
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")

        card = CardsRepository.get_card(db, checklist.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        if checklist.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        checklist_dict = data.model_dump()
        try:
            db_checklist = ChecklistRepository.patch_checklist(
                db, checklist_dict, checklist
            )
            payload = ChecklistUpdatedPayload.model_validate(
                {**db_checklist.__dict__, "card_id": card.id, "board_id": board.id}
            )
            return payload
        except Exception as e:
            ChecklistRepository.rollback(db)
            raise HTTPException(500, f"Failed to patch checklist: {str(e)}")

    @staticmethod
    def update_item(
        db, item_id: UUID, data: ChecklistItemUpdate, current_user
    ) -> ChecklistItemUpdatedPayload:
        item = ChecklistRepository.get_item(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        checklist = ChecklistRepository.get_checklist(db, item.checklist_id)
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")

        card = CardsRepository.get_card(db, checklist.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        if checklist.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        item_dict = data.model_dump()
        try:
            db_item = ChecklistRepository.patch_item(db, item_dict, item)
            payload = ChecklistItemUpdatedPayload.model_validate(
                {**db_item.__dict__, "checklist_id": checklist.id, "board_id": board.id}
            )
            return payload
        except Exception as e:
            ChecklistRepository.rollback(db)
            raise HTTPException(500, f"Failed to path checklist item: {str(e)}")

    @staticmethod
    def flag_item(
        db, item_id: UUID, data: ChecklistItemFlag, current_user
    ) -> ChecklistItemFlagPayload:
        item = ChecklistRepository.get_item(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        checklist = ChecklistRepository.get_checklist(db, item.checklist_id)
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")

        card = CardsRepository.get_card(db, checklist.card_id)
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
            db_item = ChecklistRepository.flag_item(db, data, item)
            payload = ChecklistItemFlagPayload.model_validate(
                {**db_item.__dict__, "checklist_id": checklist.id, "board_id": board.id}
            )
            return payload
        except Exception as e:
            ChecklistRepository.rollback(db)
            raise HTTPException(500, f"Failed to path checklist item: {str(e)}")

    @staticmethod
    def delete_checklist(
        db, checklist_id: UUID, current_user
    ) -> ChecklistDeletedPayload:
        checklist = ChecklistRepository.get_checklist(db, checklist_id)
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")

        card = CardsRepository.get_card(db, checklist.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        if checklist.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        try:
            db_checklist = ChecklistRepository.delete_checklist(db, checklist)
            payload = ChecklistDeletedPayload.model_validate(
                {**db_checklist.__dict__, "card_id": card.id, "board_id": board.id}
            )
            return payload
        except Exception as e:
            ChecklistRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete checklist: {str(e)}")

    @staticmethod
    def delete_item(db, item_id: UUID, current_user) -> ChecklistItemDeletedPayload:
        item = ChecklistRepository.get_item(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        checklist = ChecklistRepository.get_checklist(db, item.checklist_id)
        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")

        card = CardsRepository.get_card(db, checklist.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        if checklist.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        try:
            db_item = ChecklistRepository.delete_item(db, item)
            payload = ChecklistItemDeletedPayload.model_validate(
                {**db_item.__dict__, "checklist_id": checklist.id, "board_id": board.id}
            )
            return payload
        except Exception as e:
            ChecklistRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete checklist item: {str(e)}")
