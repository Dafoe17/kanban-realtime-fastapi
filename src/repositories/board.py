from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Board, UserBoardPreference
from src.permissions import Permission, Role


class BoardsRepository:

    @staticmethod
    def get_board(db: Session, id: UUID):
        return db.query(Board).filter(Board.id == id).first()

    @staticmethod
    def get_user_boards(db: Session, id: UUID):
        return (
            db.query(Board)
            .join(UserBoardPreference, UserBoardPreference.board_id == Board.id)
            .filter(UserBoardPreference.user_id == id)
        )

    @staticmethod
    def is_user_in_board(
        db: Session, user_id: UUID, board_id: UUID
    ) -> UserBoardPreference | None:
        query = (
            db.query(UserBoardPreference)
            .filter(UserBoardPreference.user_id == user_id)
            .filter(UserBoardPreference.board_id == board_id)
            .first()
        )
        return query

    @staticmethod
    def apply_filters(db: Session, filters: list):
        query = db.query(Board)
        if filters:
            query = query.filter(*filters)
        return query

    @staticmethod
    def apply_sorting(query, sort_attr, order: str):
        sort_attr = getattr(Board, sort_attr, Board.title)
        return query.order_by(sort_attr.desc() if order == "desc" else sort_attr.asc())

    @staticmethod
    def paginate(query, skip: int | None, limit: int | None) -> list[Board]:
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(query) -> int:
        return query.count()

    @staticmethod
    def add_board(db: Session, data) -> Board:
        board = Board(**data.model_dump())
        db.add(board)
        db.commit()
        db.refresh(board)
        return board

    @staticmethod
    def add_preferences(db: Session, data) -> UserBoardPreference:
        prefs = UserBoardPreference(**data.model_dump())
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
        return prefs

    @staticmethod
    def delete_board(db: Session, data) -> Board | None:
        db.delete(data)
        db.commit()
        return data

    @staticmethod
    def patch_board(db: Session, board: Board, data) -> Board | None:
        for key, value in data.items():
            if value is not None:
                setattr(board, key, value)
        db.commit()
        db.refresh(board)
        return board

    @staticmethod
    def patch_role_or_permissions(
        db: Session,
        user_in_board: UserBoardPreference,
        role: Role | None,
        custom_permissions: list[Permission] | None,
    ):
        if role:
            user_in_board.role = role
        if custom_permissions:
            user_in_board.custom_permissions = list(
                set(user_in_board.custom_permissions + custom_permissions)
            )
        db.commit
        db.refresh(user_in_board)
        return user_in_board

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
