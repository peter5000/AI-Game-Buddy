from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated

from app.config import settings
from app.services.cosmos_service import CosmosService

# Initialize CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security_scheme = OAuth2PasswordBearer(tokenUrl="accounts/token")
# security_scheme = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Helper function to create JWT token ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # Default 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def authenticate_user(identifier: str, password: str, cosmos_service: CosmosService) -> dict | None:
    query = "SELECT * FROM c WHERE c.email = @identifier or c.username = @identifier"
    parameters = [{"name": "@identifier", "value": identifier}]
    users = await cosmos_service.get_items_by_query(
        query=query, container_type="users", parameters=parameters
    )

    if not users:
        return None
    
    user = users[0]
    
    if not verify_password(password, user["password"]):
        return None
    
    return user

async def get_current_user_id(token: Annotated[str, Depends(security_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
       payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
       user_id: str = payload.get("sub")
       if user_id is None:
           raise credentials_exception
    except JWTError:
       raise credentials_exception
    
    return user_id
