from uuid import uuid4

from src.schemas import UserCreate

from .prefixes import USER_PREFIX


def generate_test_user(username_prefix=USER_PREFIX):
    return UserCreate(
        username=f"{username_prefix}_{uuid4().hex[:6]}",
        email=f"{username_prefix}_{uuid4().hex[:6]}@test.com",
        password_hash="password123",
    )
