import uuid

from fastapi import HTTPException

from src.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_access_token,
    verify_password,
    verify_refresh_token,
)
from src.models import User
from src.redis import TokenStorage
from src.repositories import UsersRepository
from src.schemas import UserCreate


class AuthService:

    @staticmethod
    async def login(db, email: str, password: str) -> User:

        user = UsersRepository.get_by_email(db, email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        await AuthService.create_tokens(user.id)
        return user

    @staticmethod
    async def sign_up(db, data: UserCreate):

        if UsersRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=409, detail="Email already registered")

        hashed_password = hash_password(data.password_hash)
        data.password_hash = hashed_password
        user_dict = data.model_dump()
        try:
            user = UsersRepository.add_user(db, user_dict)
            return user
        except Exception as e:
            UsersRepository.rollback(db)
            raise HTTPException(500, f"Failed to create user: {str(e)}")

    @staticmethod
    async def refresh(refresh_token: str | None):

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token missing")

        payload = verify_refresh_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Refresh token expired")

        user_id = payload.get("sub")

        stored_token = await TokenStorage.get_token(str(user_id))
        if stored_token != refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token revoked")

        new_access = create_access_token({"sub": str(user_id)})
        if not new_access:
            raise HTTPException(status_code=401, detail="Refresh token expired")

        return new_access

    @staticmethod
    async def create_tokens(id: uuid.UUID):
        access_token = create_access_token({"sub": str(id)})
        refresh_token = create_refresh_token({"sub": str(id)})
        await TokenStorage().add_token(str(id), refresh_token)

        return access_token, refresh_token

    @staticmethod
    async def logout(access_token: str | None):
        if not access_token:
            raise HTTPException(status_code=401, detail="Missing access token")

        payload = verify_access_token(access_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_id = payload.get("sub")
        await TokenStorage.delete_token(str(user_id))
