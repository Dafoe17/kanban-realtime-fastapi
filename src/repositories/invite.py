from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Invite


class InviteRepository:

    @staticmethod
    def get_invite(db: Session, invite_id: UUID) -> Invite | None:
        invite = db.query(Invite).filter_by(id=invite_id).first()
        if (
            not invite
            or (invite.expires_at and invite.expires_at < datetime.now(timezone.utc))
            or invite.max_uses == 0
        ):
            return None

        return invite

    @staticmethod
    def check_invite_exists(db: Session, board_id: UUID) -> Invite | None:
        invite = (
            db.query(Invite)
            .filter_by(board_id=board_id)
            .order_by(Invite.expires_at.desc())
            .first()
        )
        if (
            not invite
            or (invite.expires_at and invite.expires_at < datetime.now(timezone.utc))
            or invite.max_uses == 0
        ):
            return None

        return invite

    @staticmethod
    def create_invite(
        db: Session, board_id: UUID, user_id: UUID, max_uses: int
    ) -> Invite:
        invite = Invite(
            board_id=board_id, invited_by=user_id, max_uses=max_uses, is_used=False
        )
        db.add(invite)
        db.commit()
        db.refresh(invite)
        return invite

    @staticmethod
    def use_invite(db: Session, invite: Invite) -> Invite:
        invite.max_uses -= 1
        invite.is_used = True
        db.commit()
        db.refresh(invite)
        return invite

    @staticmethod
    def delete_invite(db: Session, invite: Invite) -> Invite:
        db_invite = invite
        db.delete(invite)
        db.commit()
        return db_invite

    @staticmethod
    def rollback(db: Session) -> None:
        db.rollback()
        return None
