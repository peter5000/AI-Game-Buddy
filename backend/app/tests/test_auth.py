from datetime import datetime, timedelta, timezone

import pytest
from app.auth import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_access_token,
    verify_refresh_token,
    verify_password,
)
from app.config import settings
from fastapi import HTTPException
from jose import jwt
from pydantic import SecretStr


class TestAuth:
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = SecretStr("testpassword123")
        hashed = get_password_hash(password)

        # Hash should not equal original password
        assert hashed != password

        # Verification should work
        assert verify_password(password, hashed) is True

        # Wrong password should fail
        assert verify_password(SecretStr("wrongpassword"), hashed) is False

    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": "testuser"}
        token = create_access_token(data)

        decoded = jwt.decode(
            token, settings.ACCESS_TOKEN_SECRET, algorithms=[settings.ALGORITHM]
        )

        assert decoded["sub"] == "testuser"
        assert "exp" in decoded

    def test_create_access_token_with_expiration(self):
        """Test JWT token creation with custom expiration."""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=60)
        token = create_access_token(data, expires_delta)

        decoded = jwt.decode(
            token, settings.ACCESS_TOKEN_SECRET, algorithms=[settings.ALGORITHM]
        )

        assert decoded["sub"] == "testuser"

        # Check expiration is approximately 60 minutes from now
        exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        expected_exp = datetime.now(timezone.utc) + expires_delta

        # Allow 1 minute tolerance
        assert abs((exp_time - expected_exp).total_seconds()) < 60

    def test_verify_token_valid(self):
        """Test valid token verification."""
        data = {"sub": "testuser"}
        access_token = create_access_token(data)

        payload = verify_access_token(access_token=access_token)
        user_id = payload.get("sub")
        assert user_id == "testuser"

    def test_verify_token_invalid(self):
        """Test invalid token verification."""
        invalid_token = "invalid.token.here"

        with pytest.raises(HTTPException) as exc_info:
            verify_access_token(invalid_token)

        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail

    def test_verify_token_expired(self):
        """Test expired token verification."""
        data = {"sub": "testuser"}
        expires_delta = timedelta(seconds=-1)  # Already expired
        access_token = create_access_token(data, expires_delta)

        with pytest.raises(HTTPException) as exc_info:
            verify_access_token(access_token)

        assert exc_info.value.status_code == 401

    def test_create_refresh_token(self):
        """Test refresh token creation."""
        data = {"sub": "testuser_refresh"}
        token = create_refresh_token(data)
        
        decoded = jwt.decode(
            token, settings.REFRESH_TOKEN_SECRET, algorithms=[settings.ALGORITHM]
        )
        
        assert decoded["sub"] == "testuser_refresh"
        assert "exp" in decoded

    def test_verify_refresh_token_valid(self):
        """Test valid refresh token verification."""
        data = {"sub": "testuser"}
        refresh_token = create_refresh_token(data)

        payload = verify_refresh_token(refresh_token)
        user_id = payload.get("sub")
        assert user_id == "testuser"

    def test_verify_refresh_token_invalid(self):
        """Test invalid refresh token verification."""
        invalid_token = "invalid.refresh.token"
        
        with pytest.raises(HTTPException) as exc_info:
            verify_refresh_token(invalid_token)
            
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail

    def test_verify_refresh_token_expired(self):
        """Test expired refresh token verification."""
        data = {"sub": "testuser"}
        expires_delta = timedelta(seconds=-1)  # Already expired
        refresh_token = create_refresh_token(data, expires_delta)
        
        with pytest.raises(HTTPException) as exc_info:
            verify_refresh_token(refresh_token)
            
        assert exc_info.value.status_code == 401