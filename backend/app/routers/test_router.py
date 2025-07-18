from fastapi import APIRouter, File, UploadFile, HTTPException, status, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials 
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import JWTError, jwt

from app.dependencies import cosmos_service, blob_service

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)

# Initialize CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration 
# You would store this securely in environment variables in a real application!
SECRET_KEY = "my-super-secret-key-12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token valid for 30 minutes
# END JWT Configuration 

# --- MODIFIED: Use HTTPBearer instead of OAuth2PasswordBearer ---
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="test/login") # REMOVE OR COMMENT OUT THIS LINE
security_scheme = HTTPBearer() # <<< NEW: Define HTTPBearer
# --- END MODIFIED ---

# Helper function to create JWT token ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # Default 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- MODIFIED: get_current_user_id to use HTTPAuthorizationCredentials ---
async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    # The actual token string is in credentials.credentials
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return user_id
# --- END MODIFIED ---

class TestUser(BaseModel):
    id: str
    userid: str # Partition Key
    username: str
    email: str
    password: str 

# Pydantic model for Login credentials
class UserLogin(BaseModel):
    email: EmailStr
    password: str


@router.post("/users", status_code=201)
async def create_test_user(user: TestUser):
    # Before creating a user, let's ensure the email doesn't already exist to prevent issues
    existing_users_by_email = await cosmos_service.get_items_by_query(
        query=f"SELECT * FROM c WHERE c.email = '{user.email}'",
        container_type="users"
    )
    if existing_users_by_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    # Also ensure ID is unique
    try:
        await cosmos_service.get_item(item_id=user.id, partition_key=user.userid, container_type="users")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User ID already exists")
    except HTTPException as e:
        if e.status_code != 404: # If it's not a 404 (not found), then it's some other error, re-raise
            raise

    hashed_password = pwd_context.hash(user.password)
    item_to_save = user.model_dump()
    item_to_save["password"] = hashed_password
    await cosmos_service.add_item(item=item_to_save, container_type="users")
    return {"status": "success", "message": f"User {user.id} created"}

@router.get("/users/{document_id}")
async def get_test_user(
    document_id: str,
    partition_key: str = Query(..., description="The value of the 'userid' field, which is the partition key")
):
    item = await cosmos_service.get_item(
        item_id=document_id,
        partition_key=partition_key,
        container_type="users"
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.pop("password", None) # Optionally remove password from GET response
    return item

@router.delete("/users/{document_id}" , status_code=200)
async def delete_test_user(
    document_id: str,
    partition_key: str = Query(..., description="The value of the 'userid' field, which is the partition key of the document to delete")
):
    try:
        await cosmos_service.delete_item(
            item_id=document_id,
            partition_key=partition_key,
            container_type="users"
        )
        return {"status": "success", "message": f"User '{document_id}' deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {e}")


@router.post("/query", response_model=List[Dict[str, Any]])
async def query_items(query: str):
    items = await cosmos_service.get_items_by_query(
        query=query,
        container_type="users"
    )
    if not items:
        raise HTTPException(status_code=404, detail="No items found for given query")
    return items

@router.post("/upload")
async def upload_blob(container_name: str, file: UploadFile = File(...), filename: Optional[str] = None):
    filename = filename or file.filename

    try:
        await blob_service.write_blob(container_name=container_name, filename=filename, blobstream=file.file)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Blob uploaded successfully",
                "container": container_name,
                "filename": filename
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
        
@router.post("/delete")
async def delete_blob(container_name: str, filename: str):
    try:
        await blob_service.delete_blob(container_name=container_name, filename=filename)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Blob deleted successfully",
                "container": container_name,
                "filename": filename
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# NEW POST /login ENDPOINT BELOW ---
@router.post("/login")
async def login_user(user_login: UserLogin):
    query_str = f"SELECT * FROM c WHERE c.email = '{user_login.email}'"
    users = await cosmos_service.get_items_by_query(query=query_str, container_type="users")

    if not users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_found = users[0]

    if not pwd_context.verify(user_login.password, user_found["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Login successful! Now, generate the JWT token.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_found["id"]}, # 'sub' is standard for subject (user ID)
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Endpoint Example 
@router.get("/users/me", response_model=Dict[str, Any]) # Adjust response_model if you fetch full user
async def read_users_me(current_user_id: str = Depends(get_current_user_id)):
    """
    Retrieves information about the current authenticated user.
    This endpoint requires a valid JWT access token.
    """
    # Here you would typically fetch the full user details from Cosmos DB
    # using current_user_id and the appropriate partition_key.
    # For now, we'll just return the ID from the token for demonstration.

    # Example: Fetching full user data (assuming userid is also the partition key)
    user_data = await cosmos_service.get_item(
        item_id=current_user_id,
        partition_key=current_user_id, # Assuming partition key is same as user ID
        container_type="users"
    )
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found in DB (token valid but user data missing)")
    
    user_data.pop("password", None) # Don't send hashed password back
    return user_data
# --- END NEW: Protected Endpoint ---