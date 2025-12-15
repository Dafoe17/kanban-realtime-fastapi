from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Comment


class CommentsRepository:

    @staticmethod
    def get_comment(db: Session, comment_id) -> Comment:
        return db.query(Comment).filter_by(id=comment_id).first()

    @staticmethod
    def add_comment(db: Session, data, card_id: UUID, author_id: UUID) -> Comment:
        comment = Comment(
            **data.model_dump(),
            card_id=card_id,
            author_id=author_id,
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def patch_comment(db: Session, data, comment: Comment) -> Comment:
        for key, value in data.items():
            if value is not None:
                setattr(comment, key, value)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def delete_comment(db: Session, data) -> Comment:
        db.delete(data)
        db.flush()
        db.commit()
        return data

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
