from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Column


class ColumnsRepository:

    @staticmethod
    def get_column(db: Session, column_id: UUID) -> Column:
        return db.query(Column).filter_by(column_id=column_id).first()

    @staticmethod
    def get_board_columns(db: Session, board_id: UUID):
        return db.query(Column).filter_by(board_id=board_id)

    @staticmethod
    def paginate(query, skip: int | None, limit: int | None) -> list[Column]:
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(query) -> int:
        return query.count()

    @staticmethod
    def add_column(db: Session, data, board_id: UUID) -> Column:
        column = Column(**data.model_dump(), board_id=board_id)
        db.add(column)
        db.commit()
        db.refresh(column)
        return column

    @staticmethod
    def delete_column(db: Session, data) -> Column | None:
        db.delete(data)
        db.commit()
        return data

    @staticmethod
    def patch_column(db: Session, column: Column, data) -> Column | None:
        for key, value in data.items():
            if value is not None:
                setattr(column, key, value)
        db.commit()
        db.refresh(column)
        return column

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
