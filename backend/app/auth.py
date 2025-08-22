import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Cookie, HTTPException, status
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
    return pwd_context.verify(password.get_secret_value(), hashed_password)


def get_password_hash(password: SecretStr) -> str:
    return pwd_context.hash(password.get_secret_value())


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=30
        )  # Default 30 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.ACCESS_TOKEN_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=30
        )  # Default 30 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_TOKEN_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(
    identifier: str, password: str, cosmos_service: CosmosService
) -> dict | None:
    query = "SELECT * FROM c WHERE c.email = @identifier or c.username = @identifier"
    parameters = [{"name": "@identifier", "value": identifier}]
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


async def get_user_id(access_token: Annotated[Optional[str], Cookie()] = None):
    if access_token is None:
        logger.error("JWT access token not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Missing session cookie",
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            access_token, settings.ACCESS_TOKEN_SECRET, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.error("User ID not found in JWT")
            raise credentials_exception
    except JWTError:
        logger.error("Invalid or expired JWT")
        raise credentials_exception

    return user_id
