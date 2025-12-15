from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from src.core.security import (
    JWTValidationError,
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
)


@pytest.fixture
def settings_patch(monkeypatch):
    monkeypatch.setattr(
        "src.core.security.settings.ACCESS_SECRET_KEY", "test_access_key"
    )
    monkeypatch.setattr(
        "src.core.security.settings.REFRESH_SECRET_KEY", "test_refresh_key"
    )
    monkeypatch.setattr("src.core.security.settings.ALGORITHM", "HS256")
    monkeypatch.setattr("src.core.security.settings.ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    monkeypatch.setattr("src.core.security.settings.REFRESH_TOKEN_EXPIRE_DAYS", 7)


def test_create_access_token_contains_sub_and_exp(settings_patch):
    token = create_access_token({"sub": "123"})
    decoded = jwt.decode(token, "test_access_key", algorithms=["HS256"])

    assert decoded["sub"] == "123"
    assert "exp" in decoded


def test_verify_access_token_success(settings_patch):
    token = create_access_token({"sub": "123"})
    payload = verify_access_token(token)
    assert payload
    assert payload["sub"] == "123"


def test_verify_access_token_expired(settings_patch, monkeypatch):
    expired_payload = {
        "sub": "123",
        "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
    }
    token = jwt.encode(expired_payload, "test_access_key", algorithm="HS256")

    with pytest.raises(JWTValidationError):
        assert verify_access_token(token) is None


def test_verify_access_token_invalid_signature(settings_patch):
    wrong_token = jwt.encode({"sub": "123"}, "wrong_key", algorithm="HS256")

    with pytest.raises(JWTValidationError):
        verify_access_token(wrong_token)


def test_create_refresh_token_success(settings_patch):
    token = create_refresh_token({"sub": "abc"})
    decoded = jwt.decode(token, "test_refresh_key", algorithms=["HS256"])

    assert decoded["sub"] == "abc"
    assert "exp" in decoded


def test_verify_refresh_token_success(settings_patch):
    token = create_refresh_token({"sub": "abc"})
    payload = verify_refresh_token(token)

    assert payload["sub"] == "abc"


def test_verify_refresh_token_invalid(settings_patch):
    token = "not_a_jwt"

    with pytest.raises(JWTValidationError):
        verify_refresh_token(token)
