from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.schemas import BroadcastPayload
from app.services.room_service import RoomService
from fastapi import HTTPException

# --- Test Data Constants ---
TEST_USER_ID = "user-123"
TEST_ROOM_ID = "room-abc"
TEST_GAME_TYPE = "chess"
TEST_ROOM_NAME = "Test Room"


# --- Fixtures for Mocking Dependencies ---


@pytest.fixture
def mock_cosmos_service() -> AsyncMock:
    """Provides a mock for the asynchronous CosmosService."""
    return AsyncMock()


@pytest.fixture
def mock_redis_service() -> AsyncMock:
    """Provides a mock for the asynchronous RedisService."""
    return AsyncMock()


@pytest.fixture
def mock_connection_service() -> MagicMock:
    """
    Provides a mock for ConnectionService that handles both sync and async methods.
    We start with a MagicMock (for sync methods) and then attach an AsyncMock
    for any methods that need to be awaited.
    """
    mock = MagicMock()
    # RoomService calls `broadcast` asynchronously
    mock.broadcast = AsyncMock()
    return mock


@pytest.fixture
def room_service(
    mock_cosmos_service, mock_redis_service, mock_connection_service
) -> RoomService:
    """Provides an instance of RoomService with all dependencies mocked."""
    return RoomService(
        cosmos_service=mock_cosmos_service,
        redis_service=mock_redis_service,
        connection_service=mock_connection_service,
    )


# --- Test Cases for each method ---


## Tests for create_room
class TestCreateRoom:
    """Tests for the create_room method."""
    @pytest.mark.asyncio
    async def test_create_room_success(
        self, room_service, mock_redis_service, mock_cosmos_service
    ):
        """
        Tests that a room is created successfully.
        """
        # ARRANGE: Mock that the user is not currently in any room.
        room_service.get_user_room = AsyncMock(return_value=None)

        # ACT: Call the create_room method, patching uuid to control the room_id.
        with patch("uuid.uuid4", return_value=TEST_ROOM_ID):
            created_room = await room_service.create_room(
                TEST_ROOM_NAME, TEST_GAME_TYPE, TEST_USER_ID
            )

        # ASSERT: Check that the returned Room object is correct.
        assert created_room.id == TEST_ROOM_ID
        assert created_room.name == TEST_ROOM_NAME
        assert created_room.creator_id == TEST_USER_ID
        assert TEST_USER_ID in created_room.users

        # ASSERT: Verify that data was written to Redis correctly.
        assert mock_redis_service.dict_add.call_count == 1
        assert mock_redis_service.set_add.call_count == 1
        assert (
            mock_redis_service.set_value.call_count == 2
        )  # Once for state, once for user's room.

        # ASSERT: Verify that data was written to Cosmos correctly.
        mock_cosmos_service.add_item.assert_awaited_once()
        mock_cosmos_service.patch_item.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_room_fails_if_user_already_in_room(self, room_service):
        """
        Tests that creating a room fails if the user is already in a room.
        """
        # ARRANGE: Mock that the user is already in a room.
        room_service.get_user_room = AsyncMock(return_value="existing-room")

        # ACT & ASSERT: Expect a 409 Conflict HTTPException.
        with pytest.raises(HTTPException) as exc_info:
            await room_service.create_room(TEST_ROOM_NAME, TEST_GAME_TYPE, TEST_USER_ID)

        assert exc_info.value.status_code == 409
        assert "User already in another room" in exc_info.value.detail


## Tests for join_room
class TestJoinRoom:
    """Tests for the join_room method."""
    @pytest.mark.asyncio
    async def test_join_room_success(
        self, room_service, mock_redis_service, mock_cosmos_service
    ):
        """
        Tests that a user can successfully join a room.
        """
        # ARRANGE
        joining_user_id = "user-456"
        room_service.get_user_room = AsyncMock(return_value=None)
        room_service.get_user_list = AsyncMock(return_value=["user-123"])

        # ACT
        await room_service.join_room(TEST_ROOM_ID, joining_user_id)

        # ASSERT: Redis was updated
        mock_redis_service.set_add.assert_awaited_once_with(
            key=f"room:{TEST_ROOM_ID}:users", values=[joining_user_id]
        )
        mock_redis_service.set_value.assert_awaited_once_with(
            key=f"user:{joining_user_id}:room", value=TEST_ROOM_ID
        )

        # ASSERT: Cosmos was updated twice (once for the room, once for the user)
        assert mock_cosmos_service.patch_item.call_count == 2

    @pytest.mark.asyncio
    async def test_join_room_fails_if_user_already_in_room(self, room_service):
        """
        Tests that joining a room fails if the user is already in a room.
        """
        # ARRANGE
        room_service.get_user_room = AsyncMock(return_value="existing-room")

        # ACT & ASSERT
        with pytest.raises(HTTPException) as exc_info:
            await room_service.join_room(TEST_ROOM_ID, TEST_USER_ID)

        assert exc_info.value.status_code == 409


## Tests for get_room
class TestGetRoom:
    """Tests for the get_room method."""
    @pytest.mark.asyncio
    async def test_get_room_from_cache_success(
        self, room_service, mock_redis_service, mock_cosmos_service
    ):
        """
        Tests that a room is successfully retrieved from the cache.
        """
        # ARRANGE: Simulate a full cache hit.
        mock_redis_service.dict_get_all.return_value = {
            "id": TEST_ROOM_ID,
            "room_id": TEST_ROOM_ID,
            "name": "Cached Room",
            "creator_id": "user1",
            "game_type": "chess",
        }
        mock_redis_service.set_get.return_value = {"user1"}
        mock_redis_service.get_value.return_value = "{}"

        # ACT
        room = await room_service.get_room(TEST_ROOM_ID)

        # ASSERT
        assert room is not None
        assert room.id == TEST_ROOM_ID
        assert room.name == "Cached Room"
        mock_cosmos_service.get_item.assert_not_awaited()  # Should not touch the database

    @pytest.mark.asyncio
    async def test_get_room_from_db_on_cache_miss(
        self, room_service, mock_redis_service, mock_cosmos_service
    ):
        """
        Tests that a room is successfully retrieved from the database on a cache miss.
        """
        # ARRANGE: Simulate a cache miss and a database hit.
        mock_redis_service.dict_get_all.return_value = {}  # Cache is empty
        db_data = {
            "id": TEST_ROOM_ID,
            "room_id": TEST_ROOM_ID,
            "name": "DB Room",
            "creator_id": "user1",
            "game_type": "chess",
            "users": ["user1"],
            "game_state": {},
        }
        mock_cosmos_service.get_item.return_value = db_data

        # ACT
        room = await room_service.get_room(TEST_ROOM_ID)

        # ASSERT
        assert room is not None
        assert room.name == "DB Room"
        mock_cosmos_service.get_item.assert_awaited_once()
        # ASSERT: Check that the cache was repopulated.
        mock_redis_service.dict_add.assert_awaited_once()
        mock_redis_service.set_add.assert_awaited_once()


## Tests for send_game_state
class TestSendGameState:
    """Tests for the send_game_state method."""
    @pytest.mark.asyncio
    async def test_send_game_state_success(self, room_service, mock_connection_service):
        """
        Tests that the game state is sent successfully.
        """
        # ARRANGE
        game_state = {"turn": "white"}
        initial_user_list = ["user1", "user2"]
        active_user_list = ["user1", "user2"]  # Assume both are active

        room_service.get_user_list = AsyncMock(return_value=initial_user_list)
        # Configure the synchronous get_active_users_from_list method
        mock_connection_service.get_active_users_from_list.return_value = (
            active_user_list
        )

        # ACT
        await room_service.send_game_state(TEST_ROOM_ID, game_state)

        # ASSERT
        mock_connection_service.get_active_users_from_list.assert_called_once_with(
            user_list=initial_user_list
        )

        expected_payload = BroadcastPayload(
            user_list=active_user_list, message=game_state
        )
        # Assert the async broadcast method was awaited with the correct payload
        mock_connection_service.broadcast.assert_awaited_once_with(
            payload=expected_payload
        )
