from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional
import uuid
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import timedelta

from app.dependencies import cosmos_service, blob_service
from app import auth

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token valid for 30 minutes

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())) # Partition Key
    username: str
    email: EmailStr
    password: str

# Pydantic model for Login credentials
class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/users", status_code=201)
async def create_test_user(user: UserCreate):
    print(f"Attempting to create user: '{user.username}', email: '{user.email}'")

    # Before creating a user, let's ensure the email doesn't already exist to prevent issues
    print(f"Checking for existing email: '{user.email}'")
    existing_users_by_email = await cosmos_service.get_items_by_query(
        query=f"SELECT * FROM c WHERE c.email = '{user.email}'",
        container_type="users"
    )
    print(f"Result of email query: {existing_users_by_email}")
    if existing_users_by_email:
        print("Email already registered, raising 409.")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    # Also ensure username is unique
    print(f"Checking for existing ID: '{user.username}'")
    try:
        item_from_db = await cosmos_service.get_items_by_query(
            query=f"SELECT * FROM c WHERE c.username = '{user.username}'",
            container_type="users"
        )
        print(f"Result of get_item: {item_from_db}")
        
        if len(item_from_db) == 0:
            print("Username not found (get_item returned None), proceeding with creation.")
        else: # Only raise 409 if an item WAS actually found
            print("Username already exists, raising 409 (from try block).")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    except HTTPException as e:
        print(f"Exception caught in get_item check: Status Code={e.status_code}, Detail={e.detail}")
        if e.status_code != 404: # If it's not a 404 (not found), then it's some other error, re-raise
            print("Re-raising non-404 exception.")
            raise
        else:
            print("Username not found (404 caught), proceeding with creation.")
    except Exception as e:
        print(f"Unexpected exception in get_item check: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error during ID check: {e}")

    hashed_password = auth.get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    item_to_save = new_user.model_dump()
    
    print(f"Adding new user to Cosmos DB: {item_to_save['id']}")
    await cosmos_service.add_item(item=item_to_save, container_type="users")
    print(f"User '{user.username}' created successfully.")
    return {"status": "success", "message": f"User '{user.username}' created"}

@router.get("/users/{document_id}")
async def get_test_user(document_id: str):
    item = await cosmos_service.get_item(
        item_id=document_id,
        partition_key=document_id,
        container_type="users"
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.pop("password", None) # Optionally remove password from GET response
    return item

@router.delete("/users/{document_id}" , status_code=200)
async def delete_test_user(document_id: str):
    try:
        await cosmos_service.delete_item(
            item_id=document_id,
            partition_key=document_id,
            container_type="users"
        )
        return {"status": "success", "message": f"User {document_id} deleted"}
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

    if not auth.verify_password(user_login.password, user_found["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Login successful! Now, generate the JWT token.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user_found["id"]}, # 'sub' is standard for subject (user ID)
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Endpoint Example 
@router.get("/users/me", response_model=Dict[str, Any]) # Adjust response_model if you fetch full user
async def read_users_me(current_user_id: str = Depends(auth.get_current_user_id)):
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