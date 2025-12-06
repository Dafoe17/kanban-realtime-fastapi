from fastapi import Cookie, Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.core.security import JWTValidationError, verify_access_token
from src.database import Session, Session_local
from src.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token-json")


def get_db():
    db: Session = Session_local()
    try:
        yield db
    finally:
        db.close()


def get_user_from_token(token: str | None, db: Session) -> User:

    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

    user = db.query(User).filter(User.id == payload["sub"]).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_user(
    access_token: str | None = Cookie(default=None),
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:

    token = access_token

    if not token and authorization:
        scheme, _, token_str = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token_str:
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        token = token_str

    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        return get_user_from_token(token, db)
    except JWTValidationError as e:
        raise HTTPException(status_code=401, detail=str(e))
