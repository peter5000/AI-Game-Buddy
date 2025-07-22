from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any, Annotated
from datetime import timedelta

from app.services.cosmos_service import CosmosService
from app.services.user_service import UserService
from app.dependencies import get_cosmos_service, get_user_service
from app import auth
from app.schemas import UserCreate, UserLogin

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token valid for 30 minutes

@router.post("/register", status_code=201)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    await user_service.create_user(user=user)
    return {"status": "success", "message": f"User '{user.username}' created"}

@router.post("/token")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], cosmos_service: CosmosService = Depends(get_cosmos_service)):
    user = await auth.authenticate_user(
        identifier=form_data.username,
        password=form_data.password,
        cosmos_service=cosmos_service
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user["id"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=Dict[str, Any]) # Adjust response_model if you fetch full user
async def read_users_me(current_user_id: str = Depends(auth.get_current_user_id), cosmos_service: CosmosService = Depends(get_cosmos_service)):
    """
    Retrieves information about the current authenticated user.
    This endpoint requires a valid JWT access token.
    """

    user_data = await cosmos_service.get_item(
        item_id=current_user_id,
        partition_key=current_user_id,
        container_type="users"
    )
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found in DB (token valid but user data missing)")
    
    user_data.pop("password", None) # Don't send hashed password back
    return user_data