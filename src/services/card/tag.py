from uuid import UUID

from fastapi import HTTPException

from src.permissions import Permission, check_board_permission
from src.repositories import BoardsRepository, CardsRepository, TagsRepository
from src.schemas import (
    CardTagAssociationRead,
    TagCreate,
    TagRead,
    TagsListResponse,
    TagUpdate,
)
from src.ws import (
    TagCreatedPayload,
    TagDeletedPayload,
    TagSetPayload,
    TagUpdatedPayload,
)


class TagsService:

    @staticmethod
    def get_tag(db, tag_id: UUID, board_id: UUID, current_user) -> TagRead:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board_id, Permission.BOARD_VIEW)

        tag = TagsRepository.get_tag(db, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        return TagRead.model_validate(tag)

    @staticmethod
    def get_tags_by_card(db, board_id: UUID, card_id: UUID, current_user):
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board_id, Permission.BOARD_VIEW)

        card = CardsRepository.get_card(db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        tags = TagsRepository.get_tags_by_card(db, card_id)
        if not tags:
            raise HTTPException(status_code=404, detail="No tags for card")

        response = TagsListResponse(
            total=len(tags),
            skip=None,
            limit=None,
            tags=[TagRead.model_validate(tag) for tag in tags],
        )
        return response

    @staticmethod
    def get_association(
        db, tag_id: UUID, board_id: UUID, card_id: UUID, current_user
    ) -> CardTagAssociationRead:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board_id, Permission.BOARD_VIEW)

        card = CardsRepository.get_card(db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        tag = TagsRepository.get_tag(db, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        association = TagsRepository.get_association(db, tag_id, card_id)

        return CardTagAssociationRead.model_validate(association)

    @staticmethod
    def create_tag(
        db, board_id: UUID, data: TagCreate, current_user
    ) -> TagCreatedPayload:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board_id, Permission.BOARD_WRITE)

        try:
            db_tag = TagsRepository.add_tag(db, data, board_id)
            payload = TagCreatedPayload.model_validate(
                {**db_tag.__dict__, "board_id": board_id}
            )
            return payload
        except Exception as e:
            TagsRepository.rollback(db)
            raise HTTPException(500, f"Failed to create tag: {str(e)}")

    @staticmethod
    def set_tag(
        db, board_id: UUID, card_id: UUID, tag_id: UUID, current_user
    ) -> TagSetPayload:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board_id, Permission.BOARD_WRITE)

        tag = TagsRepository.get_tag(db, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        card = CardsRepository.get_card(db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        try:
            db_tag = TagsRepository.set_tag(db, tag_id, card_id)
            payload = TagSetPayload.model_validate(
                {**db_tag.__dict__, "card_id": card_id, "board_id": board_id}
            )
            return payload
        except Exception as e:
            TagsRepository.rollback(db)
            raise HTTPException(500, f"Failed to set tag to card: {str(e)}")

    @staticmethod
    def remove_tag(
        db, board_id: UUID, card_id: UUID, tag_id: UUID, current_user
    ) -> TagSetPayload:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board_id, Permission.BOARD_WRITE)

        card = CardsRepository.get_card(db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        tag = TagsRepository.get_tag(db, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        try:
            db_association = TagsRepository.get_association(db, tag_id, card_id)
            db_tag = TagsRepository.remove_tag(db, db_association)
            payload = TagSetPayload.model_validate(
                {**db_tag.__dict__, "card_id": None, "board_id": board_id}
            )
            return payload
        except Exception as e:
            TagsRepository.rollback(db)
            raise HTTPException(500, f"Failed to remove tag from card: {str(e)}")

    @staticmethod
    def update_tag(
        db, data: TagUpdate, board_id: UUID, tag_id: UUID, current_user
    ) -> TagUpdatedPayload:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board_id, Permission.BOARD_WRITE)

        tag = TagsRepository.get_tag(db, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        tag_dict = data.model_dump()
        try:
            db_tag = TagsRepository.patch_tag(db, tag_dict, tag)
            payload = TagUpdatedPayload.model_validate(
                {**db_tag.__dict__, "board_id": board_id}
            )
            return payload
        except Exception as e:
            TagsRepository.rollback(db)
            raise HTTPException(500, f"Failed to update tag: {str(e)}")

    @staticmethod
    def delete_tag(db, board_id: UUID, tag_id: UUID, current_user) -> TagDeletedPayload:
        board = BoardsRepository.get_board(db, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        check_board_permission(db, current_user, board_id, Permission.BOARD_WRITE)

        tag = TagsRepository.get_tag(db, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        try:
            db_tag = TagsRepository.delete_tag(db, tag)
            payload = TagDeletedPayload.model_validate(
                {**db_tag.__dict__, "board_id": board_id}
            )
            return payload
        except Exception as e:
            TagsRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete tag: {str(e)}")
