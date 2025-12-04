from uuid import UUID

from sqlalchemy.orm import Session

from src.models import UserBoardPreference


class UserBoardPrefRepository:

    @staticmethod
    def check_is_member(db: Session, board_id: UUID, user_id):
        member = (
            db.query(UserBoardPreference)
            .filter(
                UserBoardPreference.board_id == board_id,
                UserBoardPreference.user_id == user_id,
            )
            .first()
        )
        if member:
            return True
        return False

    @staticmethod
    def get_pref_by_id(db: Session, pref_id: UUID) -> UserBoardPreference:
        return db.query(UserBoardPreference).filter_by(id=pref_id).first()

    @staticmethod
    def get_user_boards(db: Session, user_id: UUID):
        return db.query(UserBoardPreference).filter(
            UserBoardPreference.user_id == user_id
        )

    @staticmethod
    def patch_pref(
        db: Session, board_pref: UserBoardPreference, data
    ) -> UserBoardPreference:
        for key, value in data.items():
            if value is not None:
                setattr(board_pref, key, value)
        db.commit()
        db.refresh(board_pref)
        return board_pref

    @staticmethod
    def patch_bool_key(
        db: Session, board_pref: UserBoardPreference, key: str, value: bool
    ) -> UserBoardPreference:
        setattr(board_pref, key, value)
        db.commit()
        db.refresh(board_pref)
        return board_pref

    @staticmethod
    def count(query) -> int:
        return query.count()

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
