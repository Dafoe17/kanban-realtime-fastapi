from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Card, CardTagAssociation, Tag


class TagsRepository:
    @staticmethod
    def get_tag(db: Session, tag_id: UUID) -> Tag:
        return db.query(Tag).filter_by(id=tag_id).first()

    @staticmethod
    def get_tags_by_card(db: Session, card_id: UUID) -> list[Tag]:
        return (
            db.query(Tag)
            .join(CardTagAssociation)
            .join(Card)
            .where(Card.id == card_id)
            .all()
        )

    @staticmethod
    def get_association(db: Session, tag_id: UUID, card_id: UUID) -> CardTagAssociation:
        return (
            db.query(CardTagAssociation)
            .filter_by(tag_id=tag_id, card_id=card_id)
            .first()
        )

    @staticmethod
    def add_tag(db: Session, data, board_id: UUID) -> Tag:
        tag = Tag(**data.model_dump(), board_id=board_id)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def set_tag(db: Session, tag_id: UUID, card_id: UUID) -> CardTagAssociation:
        association = CardTagAssociation(tag_id=tag_id, card_id=card_id)
        db.add(association)
        db.commit()
        db.refresh(association)
        return association

    @staticmethod
    def remove_tag(db: Session, association: CardTagAssociation) -> CardTagAssociation:
        db.delete(association)
        db.flush()
        db.commit()
        return association

    @staticmethod
    def patch_tag(db: Session, data, tag: Tag) -> Tag:
        for key, value in data.items():
            if value is not None:
                setattr(tag, key, value)
        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def delete_tag(db: Session, tag: Tag) -> Tag:
        db.delete(tag)
        db.flush()
        db.commit()
        return tag

    @staticmethod
    def count(query) -> int:
        return query.count()

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
