from src.core.security import hash_password, verify_password


def test_hash_password_creates_different_hashes():
    password = "new_password"

    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2
    assert hash1.startswith("$argon2") or hash1.startswith("$2b$")


def test_verify_password_success():
    password = "mypassword"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_fail():
    password = "mypassword"
    hashed = hash_password(password)

    assert verify_password("wrongpass", hashed) is False
