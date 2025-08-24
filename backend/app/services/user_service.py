import logging
import uuid
import re
from fastapi import HTTPException, status

from app.schemas import UserCreate, User
from app.auth import get_password_hash
from app.services.cosmos_service import CosmosService

class UserService:
    def __init__(self, cosmos_service: CosmosService):
        self.logger = logging.getLogger(__name__)
        self.cosmos_service = cosmos_service
        
    async def create_user(self, user: UserCreate):
        self.logger.info(f"Attempting to create user: '{user.username}', email: '{user.email}'")

        # Check if username is valid
        pattern = r"^[a-zA-Z0-9_-]{3,20}$"
        if not bool(re.match(pattern, user.username)):
            self.logger.warning(f"Username '{user.username}' has invalid characters")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid username '{user.username}'")
        
        # Before creating a user, let's ensure the email doesn't already exist to prevent issues
        self.logger.info(f"Checking for existing email: '{user.email}'")
        query = "SELECT * FROM c WHERE c.email_lower = @email"
        parameters = [
            {"name": "@email", "value": user.email.lower()}
        ]

        existing_users_by_email = await self.cosmos_service.get_items_by_query(
            query=query,
            container_type="users",
            parameters=parameters
        )
        self.logger.info(f"Result of email query: {existing_users_by_email}")
        if existing_users_by_email:
            self.logger.warning("Email already registered, raising 409.")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        
        # Also ensure username is unique
        self.logger.info(f"Checking for existing ID: '{user.username}'")
        if not await self.check_user_exists(username=user.username):
            self.logger.info("Username not found (get_item returned None), proceeding with creation.")
        else: # Only raise 409 if an item WAS actually found
            self.logger.warning("Username already exists, raising 409 (from try block).")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        new_user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user.password)
        new_user = User(
            id=new_user_id,
            user_id=new_user_id,
            username=user.username,
            username_lower=user.username.lower(),
            email=user.email,
            email_lower=user.email.lower(),
            password=hashed_password
        )
        item_to_save = new_user.model_dump()
        
        self.logger.info(f"Adding new user to Cosmos DB: {item_to_save['id']}")
        await self.cosmos_service.add_item(item=item_to_save, container_type="users")
        self.logger.info(f"User '{user.username}' created successfully.")
    
    async def delete_user(self, user_id: str):
        self.logger.info(f"Deleting user '{user_id}' from Cosmos DB")
        await self.cosmos_service.delete_item(item_id=user_id, partition_key=user_id, container_type="users")
        self.logger.info(f"User '{user_id}' deleted successfully.")
    
    async def get_user_by_username(self, username: str) -> User:
        self.logger.info(f"Attempting to get user: '{username}'")
        if not username:
            raise ValueError("Missing username")
        
        try:
            query = "SELECT * FROM c WHERE c.username_lower = @username"
            parameters = [
                {"name": "@username", "value": username.lower()}
            ]
            user = await self.cosmos_service.get_items_by_query(
                query=query,
                container_type="users",
                parameters=parameters
            )
        except HTTPException as e:
            self.logger.error(f"Exception caught in get_item check: Status Code={e.status_code}, Detail={e.detail}")
            if e.status_code != 404:
                self.logger.error("Re-raising non-404 exception.")
                raise
            else:
                self.logger.warning("Username not found")
        except Exception as e:
            self.logger.error(f"Unexpected exception in get_item check: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error during ID check: {e}")
        
        if len(user) == 0:
            self.logger.info(f"Username '{username}' not found")
            return None
        elif len(user) == 1:
            self.logger.info(f"Username '{username}' found")
            return User(**user[0])
        else:
            self.logger.warning(f"Multiple users with username '{username}' found")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Multiple users with username '{username}'")
    
    async def check_user_exists(self, username: str) -> bool:
        if not username:
            raise ValueError("Missing username")
        user = await self.get_user_by_username(username)
        if user is None:
            return False
        return True
    
    # TODO: Change username/email/password functions