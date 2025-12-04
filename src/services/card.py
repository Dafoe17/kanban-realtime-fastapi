from uuid import UUID

from fastapi import HTTPException

from src.permissions import Permission, check_board_permission
from src.repositories import BoardsRepository, CardsRepository, ColumnsRepository
from src.schemas import CardCreate, CardRead, CardsListResponse, CardUpdate


class CardsService:

    @staticmethod
    def get_column_cards(column_id: UUID, db, current_user, skip: int | None):
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
    def get_card(card_id: UUID, db, current_user):
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
    def patch_card(card_id: UUID, data: CardUpdate, db, current_user):
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
            return CardRead.model_validate(db_card)
        except Exception as e:
            CardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to patch card: {str(e)}")

    @staticmethod
    def create_card(db, column_id: UUID, current_user, data: CardCreate):
        column = ColumnsRepository.get_column(db, column_id=column_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        board = BoardsRepository.get_board(db, id=column.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board.id, Permission.BOARD_WRITE)

        try:
            card = CardsRepository.add_card(db, data, column_id)
            return CardRead.model_validate(card)
        except Exception as e:
            CardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to create card: {str(e)}")

    @staticmethod
    def delete_card(db, card_id: UUID, current_user):
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
            return CardRead.model_validate(db_card)
        except Exception as e:
            CardsRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete card: {str(e)}")
