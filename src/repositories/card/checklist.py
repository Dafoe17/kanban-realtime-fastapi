from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Checklist, ChecklistItem


class ChecklistRepository:
    @staticmethod
    def get_checklist(db: Session, checklist_id: UUID) -> Checklist:
        return db.query(Checklist).filter_by(id=checklist_id).first()

    @staticmethod
    def get_item(db: Session, item_id: UUID) -> ChecklistItem:
        return db.query(ChecklistItem).filter_by(id=item_id).first()

    @staticmethod
    def add_checklist(db: Session, data, card_id: UUID, author_id: UUID) -> Checklist:
        checklist = Checklist(
            **data.model_dump(),
            card_id=card_id,
            author_id=author_id,
        )
        db.add(checklist)
        db.commit()
        db.refresh(checklist)
        return checklist

    @staticmethod
    def add_item(db: Session, data, checklist_id: UUID) -> ChecklistItem:
        item = ChecklistItem(**data.model_dump(), checklist_id=checklist_id)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def patch_checklist(db: Session, data, checklist: Checklist) -> Checklist:
        for key, value in data.items():
            if value is not None:
                setattr(checklist, key, value)
        db.commit()
        db.refresh(checklist)
        return checklist

    @staticmethod
    def patch_item(db: Session, data, item: ChecklistItem) -> ChecklistItem:
        for key, value in data.items():
            if value is not None:
                setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def flag_item(db: Session, data, item: ChecklistItem) -> ChecklistItem:
        item.status = data
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_checklist(db: Session, checklist: Checklist) -> Checklist:
        db.delete(checklist)
        db.flush()
        db.commit()
        return checklist

    @staticmethod
    def delete_item(db: Session, item: ChecklistItem) -> ChecklistItem:
        db.delete(item)
        db.flush()
        db.commit()
        return item

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
