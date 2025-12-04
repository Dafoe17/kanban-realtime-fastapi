from uuid import UUID

from fastapi import HTTPException

from src.permissions import Permission, check_board_permission
from src.repositories import BoardsRepository, CardsRepository, ColumnsRepository
from src.schemas import CardCreate, CardMove, CardRead, CardsListResponse, CardUpdate
from src.ws import (
    CardCreatedPayload,
    CardDeletedPayload,
    CardMovedPayload,
    CardUpdatedPayload,
)


class CardsService:

    @staticmethod
    def get_column_cards(
        column_id: UUID, db, current_user, skip: int | None
    ) -> CardsListResponse:
        column = ColumnsRepository.get_column(db, column_id=column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_VIEW)

        query = CardsRepository.get_column_cards(db, column_id)
        total = CardsRepository.count(query)
        cards = CardsRepository.paginate(query, skip, 5)

        response = CardsListResponse(
            total=total,
            skip=skip,
            limit=5,
            cards=[CardRead.model_validate(card) for card in cards],
        )

        return response

    @staticmethod
    def get_card(card_id: UUID, db, current_user) -> CardRead:
        card = CardsRepository.get_card(db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_VIEW)

        return CardRead.model_validate(card)

    @staticmethod
    def patch_card(
        card_id: UUID, data: CardUpdate, db, current_user
    ) -> CardUpdatedPayload:
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

        card_dict = data.model_dump()
        try:
            db_card = CardsRepository.patch_card(db, card, card_dict)
            payload = CardUpdatedPayload.model_validate(
                {**db_card.__dict__, "board_id": board.id}
            )
            payload.board_id = board.id
            return payload
        except Exception as e:
            CardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to patch card: {str(e)}")

    @staticmethod
    def move_card(card_id: UUID, data: CardMove, db, current_user) -> CardMovedPayload:
        card = CardsRepository.get_card(db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        column = ColumnsRepository.get_column(db, column_id=card.column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        db_cards = list(CardsRepository.get_column_cards(db, column.id))
        if data.position < 0 or data.position >= db_cards[-1].position:
            raise HTTPException(
                400, f"Failed to move, invalid position: {data.position}"
            )

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        card_dict = data.model_dump()
        try:
            db_card = CardsRepository.patch_card(db, card, card_dict)
            payload = CardMovedPayload.model_validate(
                {**db_card.__dict__, "board_id": board.id}
            )
            return payload
        except Exception as e:
            CardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to patch card: {str(e)}")

    @staticmethod
    def create_card(
        db, column_id: UUID, current_user, data: CardCreate
    ) -> CardCreatedPayload:
        column = ColumnsRepository.get_column(db, column_id=column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        db_cards = CardsRepository.get_last_column_card(db, column.id)
        new_position = db_cards[0] + 1 if db_cards else 0

        try:
            db_card = CardsRepository.add_card(db, data, column_id, new_position)
            payload = CardCreatedPayload.model_validate(
                {**db_card.__dict__, "board_id": board.id}
            )
            return payload
        except Exception as e:
            CardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to create card: {str(e)}")

    @staticmethod
    def delete_card(db, card_id: UUID, current_user) -> CardDeletedPayload:
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
            db_card = CardsRepository.delete_card(db, card)
            payload = CardDeletedPayload.model_validate(
                {**db_card.__dict__, "board_id": board.id}
            )
            return payload
        except Exception as e:
            CardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete card: {str(e)}")
