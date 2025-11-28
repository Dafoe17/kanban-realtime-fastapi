from src.database import Session, Session_local
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.core.security import verify_access_token, JWTValidationError
from src.models import User
from src.repositories import UsersRepository
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token-json")


def get_db():
    db: Session = Session_local()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)) -> User:
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

def require_roles(*allowed_roles: str):
    def dependency(
        db,
        board_id: UUID,
        current_user: User = Depends(get_current_user)
        ):
        user_role = UsersRepository.get_user_role_in_board(
            db,
            user_id=current_user.id,
            board_id=board_id
        )

        if not user_role or user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Allowed roles: {', '.join(allowed_roles)}"
            )
        return current_user
