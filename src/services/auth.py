from src.repositories import UsersRepository
from src.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)

class AuthService:

    @staticmethod
    def login(db, 
              identifier: str, 
              password: str, ):

        if "@" in identifier:
            user = UsersRepository.get_by_email(db, identifier)
        else:
            user = UsersRepository.get_by_username(db, identifier)

        if not user or not verify_password(password, user.password):
            return None

        return user

    @staticmethod
    def refresh(refresh_toke: str):
        payload = verify_refresh_token(refresh_toke)
        if not payload:
            return None
    
        user_id = payload.get("sub")
        new_access = create_access_token({"sub": user_id})

        return new_access
    
    @staticmethod
    def create_tokens(username: str, role: str):
        access_token = create_access_token({
            "sub": username,
            "role": role
        })

        refresh_token = create_refresh_token({
            "sub": username,
            "role": role
        })
        
        return access_token, refresh_token
         