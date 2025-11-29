from uuid import UUID

from sqlalchemy.orm import Session

from src.models import User, UserBoardPreference


class UsersRepository:

    @staticmethod
    def get_by_id(db: Session, id: UUID) -> User | None:
        return db.query(User).filter(User.id == id).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def search(search: str):
        return User.username.ilike(f"%{search}%") | User.email.ilike(f"%{search}%")

    @staticmethod
    def apply_filters(db: Session, filters: list):
        query = db.query(User)
        if filters:
            query = query.filter(*filters)
        return query

    @staticmethod
    def apply_sorting(query, sort_attr, order: str):
        sort_attr = getattr(User, sort_attr, User.username)
        return query.order_by(sort_attr.desc() if order == "desc" else sort_attr.asc())

    @staticmethod
    def paginate(query, skip: int | None, limit: int | None) -> list[User]:
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(query) -> int:
        return query.count()

    @staticmethod
    def get_user_in_board(db: Session, user_id: UUID, board_id: UUID) -> User | None:
        user_in_board = (
            db.query(UserBoardPreference)
            .filter_by(user_id=user_id, board_id=board_id)
            .first()
        )
        return user_in_board

    @staticmethod
    def add_user(db: Session, data) -> User | None:
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def patch_user(db: Session, user, data) -> User | None:
        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, data) -> User | None:
        db.delete(data)
        db.commit()
        return data

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
