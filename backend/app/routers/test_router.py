from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from datetime import timedelta

from app.services.cosmos_service import CosmosService
from app.services.blob_service import BlobService
from app.services.user_service import UserService
from app.dependencies import get_cosmos_service, get_blob_service, get_user_service
from app import auth
from app.schemas import UserCreate, UserLogin

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token valid for 30 minutes

@router.post("/users", status_code=201)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    await user_service.create_user(user=user)
    return {"status": "success", "message": f"User '{user.username}' created"}

@router.get("/users/{document_id}")
async def get_user(document_id: str, cosmos_service: CosmosService = Depends(get_cosmos_service)):
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
async def delete_user(document_id: str, cosmos_service: CosmosService = Depends(get_cosmos_service)):
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
async def query_items(query: str, cosmos_service: CosmosService = Depends(get_cosmos_service)):
    items = await cosmos_service.get_items_by_query(
        query=query,
        container_type="users"
    )
    if not items:
        raise HTTPException(status_code=404, detail="No items found for given query")
    return items

@router.post("/upload")
async def upload_blob(container_name: str, file: UploadFile = File(...), filename: Optional[str] = None, blob_service: BlobService = Depends(get_blob_service)):
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
async def delete_blob(container_name: str, filename: str, blob_service: BlobService = Depends(get_blob_service)):
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

@router.post("/login")
async def login_user(user_login: UserLogin, cosmos_service: CosmosService = Depends(get_cosmos_service)):
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

@router.get("/users/me", response_model=Dict[str, Any]) # Adjust response_model if you fetch full user
async def read_users_me(current_user_id: str = Depends(auth.get_current_user_id), cosmos_service: CosmosService = Depends(get_cosmos_service)):
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