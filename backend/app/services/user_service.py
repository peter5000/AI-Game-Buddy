import logging
from fastapi import HTTPException, status, Depends

from app.schemas import UserCreate, User
from app.auth import get_password_hash

'''
Function List
- Create user
- Get user by username
- Update user info
- Delete user
- Check if user exists
'''

class UserService:
    def __init__(self, cosmos_service):
        self.logger = logging.getLogger("CosmosService")
        self.cosmos_service = cosmos_service
        
    async def create_user(self, user: UserCreate):
        self.logger.info(f"Attempting to create user: '{user.username}', email: '{user.email}'")

        # Before creating a user, let's ensure the email doesn't already exist to prevent issues
        self.logger.info(f"Checking for existing email: '{user.email}'")
        existing_users_by_email = await self.cosmos_service.get_items_by_query(
            query=f"SELECT * FROM c WHERE c.email = '{user.email}'",
            container_type="users"
        )
        self.logger.info(f"Result of email query: {existing_users_by_email}")
        if existing_users_by_email:
            self.logger.warning("Email already registered, raising 409.")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        
        # Also ensure username is unique
        self.logger.info(f"Checking for existing ID: '{user.username}'")
        if (await self.check_user_exists(username=user.username) == False):
            self.logger.info("Username not found (get_item returned None), proceeding with creation.")
        else: # Only raise 409 if an item WAS actually found
            self.logger.warning("Username already exists, raising 409 (from try block).")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        hashed_password = get_password_hash(user.password)
        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        item_to_save = new_user.model_dump()
        
        self.logger.info(f"Adding new user to Cosmos DB: {item_to_save['id']}")
        await self.cosmos_service.add_item(item=item_to_save, container_type="users")
        self.logger.info(f"User '{user.username}' created successfully.")
    
    async def delete_user(self):
        return
    
    
    async def get_user_by_username(self, username: str) -> User:
        self.logger.info(f"Attempting to get user: '{username}'")
        if not username:
            raise ValueError("Missing username")
        
        try:
            user = await self.cosmos_service.get_items_by_query(
                query=f"SELECT * FROM c WHERE c.username = '{username}'",
                container_type="users"
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
        if user == None:
            return False
        return True
    