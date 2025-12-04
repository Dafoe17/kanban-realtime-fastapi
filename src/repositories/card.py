from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Card


class CardsRepository:

    @staticmethod
    def get_card(db: Session, card_id: UUID) -> Card:
        return db.query(Card).filter_by(id=card_id).first()

    @staticmethod
    def get_column_cards(db: Session, column_id: UUID):
        return db.query(Card).filter_by(column_id=column_id).order_by(Card.position)

    @staticmethod
    def get_last_column_card(db: Session, column_id: UUID):
        return (
            db.query(Card.position)
            .filter_by(column_id=column_id)
            .order_by(Card.position.desc())
            .first()
        )

    @staticmethod
    def paginate(query, skip: int | None, limit: int | None) -> list[Card]:
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(query) -> int:
        return query.count()

    @staticmethod
    def add_card(db: Session, data, column_id: UUID, new_position: int) -> Card:
        card = Card(
            **data.model_dump(),
            column_id=column_id,
            position=new_position,
            assigned_to=None,
        )
        db.add(card)
        db.commit()
        db.refresh(card)
        return card

    @staticmethod
    def delete_card(db: Session, data) -> Card:
        db.delete(data)
        db.commit()
        return data

    @staticmethod
    def patch_card(db: Session, card: Card, data) -> Card:
        for key, value in data.items():
            if value is not None:
                setattr(card, key, value)
        db.commit()
        db.refresh(card)
        return card

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
