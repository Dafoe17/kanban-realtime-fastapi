from fastapi import HTTPException
from src.repositories import UsersRepository
from src.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    hash_password
)

class AuthService:

    @staticmethod
    def login(db, 
              email: str, 
              password: str
              ):
        
        user = UsersRepository.get_by_email(db, email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user
    
    @staticmethod
    def sign_up(db,
                data):
        
        if UsersRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=409, detail="Email already registered")
        
        hashed_password = hash_password(data.password_hash)
        data.password_hash = hashed_password
        user_dict = data.dict()
        try:
            user = UsersRepository.add_user(db, user_dict)
            return user
        except Exception as e:
            UsersRepository.rollback(db)
            raise HTTPException(500, f"Failed to create user: {str(e)}")

    @staticmethod
    def refresh(refresh_token: str):

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token missing")

        payload = verify_refresh_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Refresh token expired")
    
        user_id = payload.get("sub")
        new_access = create_access_token({"sub": user_id})
        if not new_access:
            raise HTTPException(status_code=401, detail="Refresh token expired")

        return new_access
    
    @staticmethod
    def create_tokens(email: str):
        access_token = create_access_token({
            "sub": email
        })

        refresh_token = create_refresh_token({
            "sub": email
        })
        
        return access_token, refresh_token
         