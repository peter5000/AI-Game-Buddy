import logging
import re
import uuid
from typing import Any

from fastapi import HTTPException, status

from app.auth import get_password_hash
from app.schemas import User, UserCreate
from app.services.cosmos_service import CosmosService

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, cosmos_service: CosmosService):
        self._cosmos_service = cosmos_service

    async def create_user(self, user: UserCreate) -> dict[str, Any]:
        logger.info(
            f"Attempting to create user: '{user.username}', email: '{user.email}'"
        )

        # Check if username is valid
        pattern = r"^[a-zA-Z0-9_-]{3,20}$"
        if not bool(re.match(pattern, user.username)):
            logger.warning(f"Username '{user.username}' has invalid characters")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid username '{user.username}'",
            )

        # Before creating a user, let's ensure the email doesn't already exist to prevent issues
        logger.info(f"Checking for existing email: '{user.email}'")
        query = "SELECT * FROM c WHERE c.email_lower = @email"
        parameters = [{"name": "@email", "value": user.email.lower()}]

        existing_users_by_email = await self._cosmos_service.get_items_by_query(
            query=query, container_type="users", parameters=parameters
        )
        logger.info(f"Result of email query: {existing_users_by_email}")
        if existing_users_by_email:
            logger.warning("Email already registered, raising 409.")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

        # Also ensure username is unique
        logger.info(f"Checking for existing ID: '{user.username}'")
        if not await self.check_user_exists(username=user.username):
            logger.info(
                "Username not found (get_item returned None), proceeding with creation."
            )
        else:  # Only raise 409 if an item WAS actually found
            logger.warning("Username already exists, raising 409 (from try block).")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            )

        new_user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user.password)
        new_user = User(
            id=new_user_id,
            user_id=new_user_id,
            username=user.username,
            username_lower=user.username.lower(),
            email=user.email,
            email_lower=user.email.lower(),
            password=hashed_password,
        )
        item = new_user.model_dump()

        logger.info(f"Adding new user to Cosmos DB: {item['id']}")
        await self._cosmos_service.add_item(item=item, container_type="users")
        logger.info(f"User '{user.username}' created successfully.")

        new_item = item.copy()
        new_item.pop("password", None)

        return new_item

    async def delete_user(self, user_id: str):
        logger.info(f"Deleting user '{user_id}' from Cosmos DB")
        await self._cosmos_service.delete_item(
            item_id=user_id, partition_key=user_id, container_type="users"
        )
        logger.info(f"User '{user_id}' deleted successfully.")

    async def get_user_by_username(self, username: str) -> User:
        logger.info(f"Attempting to get user: '{username}'")
        if not username:
            raise ValueError("Missing username")

        try:
            query = "SELECT * FROM c WHERE c.username_lower = @username"
            parameters = [{"name": "@username", "value": username.lower()}]
            user = await self._cosmos_service.get_items_by_query(
                query=query, container_type="users", parameters=parameters
            )
        except HTTPException as e:
            logger.error(
                f"Exception caught in get_item check: Status Code={e.status_code}, Detail={e.detail}"
            )
            if e.status_code != 404:
                logger.error("Re-raising non-404 exception.")
                raise
            else:
                logger.warning("Username not found")
        except Exception as e:
            logger.error(f"Unexpected exception in get_item check: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error during ID check: {e}",
            )

        if len(user) == 0:
            logger.info(f"Username '{username}' not found")
            return None
        elif len(user) == 1:
            logger.info(f"Username '{username}' found")
            return User(**user[0])
        else:
            logger.warning(f"Multiple users with username '{username}' found")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Multiple users with username '{username}'",
            )

    async def check_user_exists(self, username: str) -> bool:
        if not username:
            raise ValueError("Missing username")
        user = await self.get_user_by_username(username)
        if user is None:
            return False
        return True

    # TODO: Change username/email/password functions
