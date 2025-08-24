"""app/services/room_service.py

This module defines the RoomService, which is responsible for managing
the business logic and state of game rooms.
"""

import json
import logging
import uuid
from typing import Any, Optional

from app.schemas import BroadcastPayload, Room
from app.services.connection_service import ConnectionService
from app.services.cosmos_service import CosmosService
from app.services.redis_service import RedisService


class RoomService:
    """Manages the business logic and real-time state of game rooms.

    Attributes:
        logger (logging.Logger): Logger instance for service operations.
        cosmos_service (CosmosService): Service for persistent database storage.
        redis_service (RedisService): Service for caching and fast in-memory operations.
        connection_service (ConnectionService): Service for broadcasting WebSocket messages.
    """

    def __init__(
        self,
        cosmos_service: CosmosService,
        redis_service: RedisService,
        connection_service: ConnectionService,
    ):
        """Initializes the room service with it's dependencies.

        Args:
            cosmos_service (CosmosService): The service for interacting with Cosmos DB.
            redis_service (RedisService): The service for interacting with Redis.
            connection_manager (ConnectionManager): The service for managing websocket connections and broadcasting events.
        """
        self.logger = logging.getLogger(__name__)
        self.cosmos_service = cosmos_service
        self.redis_service = redis_service
        self.connection_service = connection_service

    async def create_room(self, room_name: str, game_type: str, user_id: str) -> Room:
        """Creates a room and stores inside redis and cosmos.

        Args:
            room_name (str): The name of the room.
            game_type (str): The type of game room is hosting.
            user_id (str): The user creating the room.

        Raises:
            ValueError: If the user ID or game type is missing.

        Returns:
            str: The room ID of the room.
        """
        if not game_type:
            raise ValueError("Game type missing on room creation")
        if not user_id:
            raise ValueError("User ID missing on room creation")

        if await self.get_user_room(user_id=user_id):
            self.logger.warning(f"User '{user_id}' currently in another room")
            return ""

        room_id = str(uuid.uuid4())

        room = Room(
            id=room_id,
            room_id=room_id,
            name=room_name,
            creator_id=user_id,
            game_type=game_type,
            users=[user_id],
        )

        cosmos_room = room.model_dump(mode="json")
        redis_room = room.model_dump(exclude={"users", "game_state"}, mode="json")

        # Write new room into redis
        await self.redis_service.dict_add(key=f"room:{room_id}", mapping=redis_room)
        await self.redis_service.expire(f"room:{room_id}", 86400)

        await self.redis_service.set_add(key=f"room:{room_id}:users", values=room.users)
        await self.redis_service.expire(f"room:{room_id}:users", 86400)

        await self.redis_service.set_value(key=f"room:{room_id}:state", value="{}")
        await self.redis_service.expire(f"room:{room_id}:users", 86400)

        # Write user into new room
        await self.redis_service.set_value(key=f"user:{user_id}:room", value=room_id)

        # Write new room into cosmos
        await self.cosmos_service.add_item(item=cosmos_room, container_type="rooms")

        # Add current room to user information
        patch_operation = [{"op": "add", "path": "/room", "value": room_id}]

        await self.cosmos_service.patch_item(
            item_id=user_id,
            partition_key=user_id,
            patch_operations=patch_operation,
            container_type="users",
        )

        return room

    async def join_room(self, room_id: str, user_id: str):
        """Joins a room.

        Args:
            room_id (str): The room ID of the room to join.
            user_id (str): The user ID of the user joining.

        Raises:
            ValueError: If the room ID, user ID or user list of room is missing.
        """
        if not room_id:
            raise ValueError("Room ID missing on join room")
        if not user_id:
            raise ValueError("User ID missing on join room")

        if await self.get_user_room(user_id=user_id):
            self.logger.warning(
                f"User '{user_id}' currently in another room, unable to join {room_id}"
            )
            return

        user_list = await self.get_user_list(room_id=room_id)

        if user_list is None:
            self.logger.error("User list not found in redis and cosmos")
            raise ValueError("User list missing in redis and cosmos")

        await self.redis_service.set_add(key=f"room:{room_id}:users", values=[user_id])
        await self.redis_service.set_value(key=f"user:{user_id}:room", value=room_id)

        # Add user to room list
        patch_operation = [{"op": "add", "path": "/users/-", "value": user_id}]

        await self.cosmos_service.patch_item(
            item_id=room_id,
            partition_key=room_id,
            patch_operations=patch_operation,
            container_type="rooms",
        )

        # Add current room to user information
        patch_operation = [{"op": "add", "path": "/room", "value": room_id}]

        await self.cosmos_service.patch_item(
            item_id=user_id,
            partition_key=user_id,
            patch_operations=patch_operation,
            container_type="users",
        )

    async def leave_room(self, room_id: str, user_id: str):
        """Leaves a room.

        Args:
            room_id (str): The room ID of the room to leave.
            user_id (str): The user ID of the user leaving the room.

        Raises:
            ValueError: If the room ID or user ID is missing.
        """
        if not room_id:
            raise ValueError("Room ID missing on leave room")
        if not user_id:
            raise ValueError("User ID missing on leave room")

        room = await self.get_room(room_id=room_id)

        # Only user in room, delete room
        if len(room.users) == 1:
            self.logger.info(f"No more users in room '{room_id}', deleting room")
            await self.delete_room(room_id=room_id)
            return

        if room is None:
            self.logger.warning(
                f"Room '{room_id}' not found when leaving for user '{user_id}'"
            )
            return

        await self.redis_service.set_remove(
            key=f"room:{room_id}:users", values=[user_id]
        )

        await self.redis_service.delete_keys(keys=[f"user:{user_id}:room"])

        try:
            item = await self.cosmos_service.get_item(
                item=room_id, partition_key=room_id
            )
            user_list = item.get("users", [])

            if user_list:
                index_to_remove = user_list.index(user_id)

                patch_operation = [
                    {"op": "remove", "path": f"/users/{index_to_remove}"}
                ]

                await self.cosmos_service.patch_item(
                    item_id=room_id,
                    partition_key=room_id,
                    patch_operations=patch_operation,
                    container_type="rooms",
                )

            self.logger.warning(f"User list not found in cosmos for room '{room_id}'")
        except ValueError:
            self.logger.warning(
                f"Tag '{room_id}' not found in the list, no changes made."
            )
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

        patch_operation = [{"op": "remove", "path": "/room"}]

        await self.cosmos_service.patch_item(
            item_id=user_id,
            partition_key=user_id,
            patch_operations=patch_operation,
            container_type="users",
        )

    async def get_room(self, room_id: str) -> Optional[Room]:
        """Gets room data from database.

        Args:
            room_id (str): The room ID of the room to get.

        Returns:
            Optional[dict]: The room data of the room.
        """
        try:
            room_data = await self.redis_service.dict_get_all(key=f"room:{room_id}")
            user_set = await self.redis_service.set_get(key=f"room:{room_id}:users")
            game_state = await self.redis_service.get_value(key=f"room:{room_id}:state")
            if room_data and user_set is not None and game_state is not None:
                # Combine the data into a single dictionary
                full_room_data = room_data | {
                    "users": user_set,
                    "game_state": json.loads(game_state),
                }
                return Room.model_validate(full_room_data)

        except Exception as e:
            self.logger.warning(
                f"Failed to reconstruct room from Redis for '{room_id}': {e}. Fetching from DB"
            )

        self.logger.info(f"Room '{room_id}' is incomplete in cache, checking database")

        room_data_from_db = await self.cosmos_service.get_item(
            item_id=room_id, partition_key=room_id, container_type="rooms"
        )

        if room_data_from_db:
            try:
                room_object = Room.model_validate(room_data_from_db)
                self.logger.info(f"Restoring room '{room_id}' to Redis cache.")

                # Separate the data for storage
                room_data = room_object.model_dump(
                    exclude={"users", "game_state"}, mode="json"
                )

                # Write to the separate Redis keys
                await self.redis_service.dict_add(
                    key=f"room:{room_id}", mapping=room_data
                )
                await self.redis_service.set_add(
                    key=f"room:{room_id}:users", values=room_object.users
                )
                await self.redis_service.set_value(
                    key=f"room:{room_id}:state",
                    value=json.dumps(room_object.game_state),
                )

                return room_object
            except Exception as e:
                self.logger.error(f"Invalid room data in CosmosDB for '{room_id}': {e}")
                return None

        self.logger.warning(f"Room '{room_id}' not found in any data source.")
        return None

    async def delete_room(self, room_id: str):
        """Deletes all room information from the redis and cosmos database.

        Args:
            room_id (str): The room ID of the room to delete.

        Raises:
            ValueError: If the room ID is missing.
        """
        if not room_id:
            raise ValueError("Room ID missing on room deletion")

        room_key = f"room:{room_id}"

        keys_to_delete: list[str] = [room_key]
        user_list = await self.get_user_list(room_id=room_id)

        # Getting all keys for user room in redis
        for user_id in user_list:
            keys_to_delete.append(f"user:{user_id}:room")

        # Get all room keys in redis
        keys_to_delete += await self.redis_service.scan_keys(key=room_key)

        # Deleting all keys in redis
        await self.redis_service.delete_keys(keys=keys_to_delete)

        # Deleting room in cosmos
        await self.cosmos_service.delete_item(
            item_id=room_id, partition_key=room_id, container_type="rooms"
        )

        # Deleting room from user information in cosmos
        for user_id in user_list:
            patch_operation = [{"op": "remove", "path": "/room"}]

            await self.cosmos_service.patch_item(
                item_id=user_id,
                partition_key=user_id,
                patch_operations=patch_operation,
                container_type="users",
            )

        # TODO: Make a publish in redis into room_update channel for room deletions locally

        self.logger.info(f"Successfully deleted room '{room_id}' in database")

    async def set_game_state(self, room_id: str, game_state: dict):
        """Sets the game state in redis and cosmos database.

        Args:
            room_id (str): The room ID of the room to set the game state of.
            game_state (dict): The game state to set.

        Raises:
            ValueError: If the room ID is missing.
        """
        if not room_id:
            raise ValueError("Room ID missing on setting game state")

        await self.redis_service.set_value(
            key=f"room:{room_id}:state", value=json.dumps(game_state)
        )
        await self.redis_service.expire(f"room:{room_id}:state", 86400)

        patch_operation = [{"op": "add", "path": "/game_state", "value": game_state}]

        await self.cosmos_service.patch_item(
            item_id=room_id,
            partition_key=room_id,
            patch_operations=patch_operation,
            container_type="rooms",
        )

    async def get_game_state(self, room_id: str) -> Optional[dict]:
        """Gets the game state from redis or cosmos database.

        Args:
            room_id (str): The room ID of the room to get the game state of.

        Raises:
            ValueError: If the room ID is missing.

        Returns:
            Optional[dict]: The game state of the room.
        """
        if not room_id:
            raise ValueError("Room ID missing on getting game state")

        game_state_json = await self.redis_service.get_value(
            key=f"room:{room_id}:state"
        )

        game_state = json.loads(game_state_json)

        if game_state is not None:
            return game_state

        self.logger.warning("Game state not found in redis, checking cosmos")
        room_data = await self.cosmos_service.get_item(
            item_id=room_id, partition_key=room_id, container_type="rooms"
        )

        if room_data is not None:
            game_state = room_data.get("game_state")

            if game_state is not None:
                self.logger.info("Game state found in cosmos, adding into redis")
                await self.redis_service.dict_add(
                    key=f"room:{room_id}:state", mapping=game_state
                )
                return game_state

        self.logger.warning(
            f"Game state not found in both redis and cosmos for room '{room_id}'"
        )
        return None

    async def delete_game_state(self, room_id: str):
        """Deletes the game state from both cosmos and redis

        Args:
            room_id (str): The room ID of the room to remove the game state from.
        """
        if not room_id:
            raise ValueError("Room ID missing on getting game state")

        await self.redis_service.delete_keys(keys=[f"room:{room_id}:state"])

        patch_operation = [{"op": "remove", "path": "/game_state"}]

        await self.cosmos_service.patch_item(
            item_id=room_id,
            partition_key=room_id,
            patch_operations=patch_operation,
            container_type="rooms",
        )

    async def send_game_state(self, room_id: str, game_state: Optional[dict]):
        """Sends the game state to all local user connections.

        Args:
            room_id (str): The room ID of the room to send the game state to.
            game_state (Optional[dict]): The game state to send to the users in the room.

        Raises:
            ValueError: If the room ID or game state is missing.
        """
        if not room_id:
            raise ValueError("Room ID missing on sending game state")

        room_list = await self.get_user_list(room_id=room_id)
        if room_list is None:
            self.logger.warning(f"Room '{room_id}' not found in room connections")
            return

        if game_state is None:
            game_state = await self.get_game_state(room_id=room_id)
            if game_state is None:
                raise ValueError(
                    f"Game state missing and not not found in database for room '{room_id}'"
                )

        # Get list of users connected through websocket endpoint on the server
        user_list = self.connection_service.get_active_users_from_list(
            user_list=room_list
        )
        self.logger.info(f"Sending game state to room '{room_id}'")

        payload = BroadcastPayload(user_list=user_list, message=game_state)
        await self.connection_service.broadcast(payload=payload)

    async def get_user_room(self, user_id: str) -> Optional[str]:
        """Gets the room ID of the room that the user is in.

        Args:
            user_id (str): The user ID of the user to get the room of.

        Raises:
            ValueError: If the user ID is missing.

        Returns:
            Optional[str]: The room ID of the user.
        """
        if not user_id:
            raise ValueError("User ID cannot be empty")

        room_id = await self.redis_service.get_value(key=f"user:{user_id}:room")
        if room_id:
            self.logger.info(f"User '{user_id}' room found in redis: {room_id}")
            return room_id

        self.logger.warning("User room not found in redis, checking cosmos")
        user_data = await self.cosmos_service.get_item(
            item_id=user_id, partition_key=user_id, container_type="users"
        )

        if user_data:
            room_id = user_data.get("room")

            if room_id:
                self.logger.info("User room found in cosmos, adding into redis")
                await self.redis_service.set_value(
                    key=f"user:{room_id}:room", value=room_id
                )
                return room_id

        self.logger.warning(
            f"User room not found in both redis and cosmos for user '{user_id}'"
        )
        return None

    async def get_user_list(self, room_id: str) -> Optional[set]:
        """Gets the list of users in the room.

        Args:
            room_id (str): The room ID of the room to get the list of users of.

        Raises:
            ValueError: If the room ID is missing.

        Returns:
            Optional[set]: The list of users in the room.
        """
        if not room_id:
            raise ValueError("Room ID missing on getting user list")

        user_list = await self.redis_service.set_get(key=f"room:{room_id}:users")

        if user_list is not None:
            return user_list

        self.logger.warning("User list not found in redis, checking cosmos")
        room_data = await self.cosmos_service.get_item(
            item_id=room_id, partition_key=room_id, container_type="rooms"
        )

        if room_data is not None:
            user_list = room_data.get("users")

            if user_list is not None:
                self.logger.info("User list found in cosmos, adding into redis")
                await self.redis_service.set_add(
                    key=f"room:{room_id}:users", values=user_list
                )
                return user_list

        self.logger.warning(
            f"User list not found in both redis and cosmos for room '{room_id}'"
        )
        return None

    async def get_all_rooms(self) -> list[dict[str, Any]]:
        """Gets all the rooms from the cosmos database.

        Returns:
            list[dict[str, Any]]: The list of all the rooms.
        """
        query = "SELECT * FROM c"
        room_list = await self.cosmos_service.get_items_by_query(
            query=query, container_type="rooms"
        )
        return room_list

    async def check_user_in_room(self, user_id: str, room_id: str) -> bool:
        """Check if user is in a room.

        Args:
            room_id (str): The room ID of the room to check.
            user_id (str): The user ID of the user to check.

        Raises:
            ValueError: If the room ID or user ID is missing.
        """
        if not room_id:
            raise ValueError("Room ID missing on checking room")
        if not user_id:
            raise ValueError("User ID missing on checking room")

        room = await self.redis_service.get_value(key=f"user:{user_id}:room")
        return room == room_id
