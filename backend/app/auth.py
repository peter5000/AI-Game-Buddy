"""auth.py

This module provides user authentication, password hashing, JWT token management, and user identification for both HTTP
and WebSocket connections.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Cookie, HTTPException, WebSocket, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import SecretStr

from app.config import settings
from app.services.cosmos_service import CosmosService

logger = logging.getLogger(__name__)

# Initialize CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# security_scheme = OAuth2PasswordBearer(tokenUrl="accounts/token")
# security_scheme = HTTPBearer()


def verify_password(password: SecretStr, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password.

    Args:
        password (SecretStr): The plain text password to verify.
        hashed_password (str): The bcrypt hashed password to verify against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(password.get_secret_value(), hashed_password)


def get_password_hash(password: SecretStr) -> str:
    """Generate a bcrypt hash for a plain text password.

    Args:
        password (SecretStr): The plain text password to hash.

    Returns:
        str: The bcrypt hashed password string suitable for database storage.
    """
    return pwd_context.hash(password.get_secret_value())


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token for user authentication.

    Args:
        data (dict): Dictionary containing user data to encode in the token.
        expires_delta (timedelta | None, optional): Custom expiration time for the token.

    Returns:
        str: The encoded JWT access token string.

    Note:
        The token includes an 'exp' (expiration) claim set to UTC time.
        Uses the ACCESS_TOKEN_SECRET from settings for signing.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)  # Default 30 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.ACCESS_TOKEN_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(access_token: str) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            access_token, settings.ACCESS_TOKEN_SECRET, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.error("Invalid or expired JWT")
        raise credentials_exception from e


def verify_refresh_token(refresh_token: str) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            refresh_token,
            settings.REFRESH_TOKEN_SECRET,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError as e:
        logger.error("Invalid or expired refresh token")
        raise credentials_exception from e


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT refresh token for token renewal.

    Args:
        data (dict): Dictionary containing user data to encode in the token.
        expires_delta (timedelta | None, optional): Custom expiration time for the token.

    Returns:
        str: The encoded JWT refresh token string.

    Note:
        The token includes an 'exp' (expiration) claim set to UTC time.
        Uses the REFRESH_TOKEN_SECRET from settings for signing.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=14)  # Default 14 days
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_TOKEN_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(
    identifier: str, password: str, cosmos_service: CosmosService
) -> dict | None:
    """Authenticate a user using email/username and password.

    Args:
        identifier (str): The user's email address or username.
        password (str): The plain text password to verify.
        cosmos_service (CosmosService): Service for database operations.

    Returns:
        dict | None: The user record dictionary if authentication succeeds,
                    None if authentication fails (user not found or wrong password).

    Raises:
        Exception: May raise database-related exceptions from cosmos_service operations.

    Note:
        Authentication failures are logged for security monitoring.
    """
    query = "SELECT * FROM c WHERE c.email_lower = @identifier or c.username_lower = @identifier"
    parameters = [{"name": "@identifier", "value": identifier.lower()}]
    users = await cosmos_service.get_items_by_query(
        query=query, container_type="users", parameters=parameters
    )

    if not users:
        logger.warning("User username or email not found")
        return None

    user = users[0]

    if not verify_password(password, user["password"]):
        logger.warning("User password is incorrect")
        return None

    logger.info(f"User '{user['username']}' authenticated")
    return user


async def get_user_id_http(
    access_token: Annotated[str | None, Cookie()] = None,
) -> str | None:
    """Extract user ID from JWT access token in HTTP requests.

    Args:
        access_token (Optional[str], optional): JWT access token from the 'access_token' cookie.
                                              Automatically injected by FastAPI from the cookie.

    Returns:
        str | None: The user ID extracted from the token.

    Raises:
        HTTPException: 401 Unauthorized if:
            - No access token cookie is present
            - Token is invalid or expired
            - Token doesn't contain a user ID ('sub' claim)

    Note:
        The function expects the user ID to be stored in the 'sub' (subject) claim of the JWT.
    """
    if access_token is None:
        logger.error("JWT access token not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Missing session cookie",
        )

    payload = verify_access_token(access_token=access_token)
    user_id = payload.get("sub")

    if user_id is None:
        logger.error("User ID not found in JWT")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def get_user_id_websocket(websocket: WebSocket) -> str | None:
    """Extract user ID from JWT access token in WebSocket connections.

    Args:
        websocket (WebSocket): The WebSocket connection object containing cookies.

    Returns:
        str | None: The user ID extracted from the token.

    Raises:
        HTTPException: 401 Unauthorized if:
            - No access token cookie is present in the WebSocket connection
            - Token is invalid or expired
            - Token doesn't contain a user ID ('sub' claim)

    Note:
        The function expects the user ID to be stored in the 'sub' (subject) claim of the JWT.
        WebSocket connections must include the access_token cookie when establishing the connection.
    """
    access_token = websocket.cookies.get("access_token")
    if access_token is None:
        logger.error("JWT access token not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Missing session cookie",
        )

    payload = verify_access_token(access_token=access_token)
    user_id = payload.get("sub")

    if user_id is None:
        logger.error("User ID not found in JWT")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id
