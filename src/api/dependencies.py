from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.core.security import JWTValidationError, verify_access_token
from src.database import Session, Session_local
from src.models import User
from src.permissions import ROLE_PERMISSIONS, Permission
from src.repositories import UsersRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token-json")


def get_db():
    db: Session = Session_local()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = verify_access_token(token)

    except JWTValidationError as e:
        raise HTTPException(status_code=401, detail=str(e))

    if not payload:
        raise HTTPException(status_code=401, detail="Token expired")

    user = db.query(User).filter(User.id == payload["sub"]).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_rule(allowed: Permission):
    def dependency(
        db,
        board_id: UUID,
        allowed: Permission,
        current_user: User = Depends(get_current_user),
    ):
        user_in_board = UsersRepository.get_user_in_board(
            db, user_id=current_user.id, board_id=board_id
        )
        if not user_in_board:
            raise HTTPException(status_code=403, detail="Access denied")

        base_rules = ROLE_PERMISSIONS[user_in_board.role]
        custom_rules = {Permission(p) for p in user_in_board.custom_permissions}
        all_rules = {*base_rules, *custom_rules}
        if not user_in_board or allowed not in all_rules:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
