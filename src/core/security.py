from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import settings

argon2id_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=19456,
    argon2__time_cost=2,
    argon2__parallelism=1,
)


class JWTValidationError(Exception):
    def __init__(self, detail: str, status_code: int = 401):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


def hash_password(password: str) -> str:
    return argon2id_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return argon2id_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM
    )


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM
    )


def verify_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        exp_timestamp = payload.get("exp")
        if exp_timestamp is None:
            return None
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        return payload if exp_datetime >= datetime.now(timezone.utc) else None
    except JWTError:
        raise JWTValidationError("Invalid token", status_code=401)


def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise JWTValidationError("Invalid token", status_code=401)
