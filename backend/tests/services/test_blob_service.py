from unittest.mock import AsyncMock, MagicMock

import pytest
from app.services import blob_service
from azure.core.exceptions import ResourceNotFoundError

# --- Mocks for Azure SDK objects ---


@pytest.fixture
def mock_blob_client() -> AsyncMock:
    """Provides an AsyncMock for a single BlobClient, which handles async I/O."""
    mock_stream = AsyncMock()
    mock_stream.readall.return_value = b"test blob content"

    mock = AsyncMock()
    mock.download_blob.return_value = mock_stream
    return mock


@pytest.fixture
def mock_container_client(mock_blob_client: AsyncMock) -> MagicMock:
    """
    Provides a MagicMock for a ContainerClient.
    Its method to get a child client is sync, but its I/O methods are async.
    """
    mock = MagicMock()
    mock.get_blob_client.return_value = mock_blob_client
    # Explicitly make the I/O methods async
    mock.get_container_properties = AsyncMock()
    mock.create_container = AsyncMock()
    return mock


@pytest.fixture
def mock_blob_service_client(mock_container_client: MagicMock) -> MagicMock:
    """
    Provides a MagicMock for the main BlobServiceClient.
    Its method to get a child client is sync, but its close method is async.
    """
    mock = MagicMock()
    mock.get_container_client.return_value = mock_container_client
    mock.close = AsyncMock()
    return mock


# --- Tests for the __init__ method ---


class TestBlobServiceInitialization:
    """Tests for the initialization of the BlobService."""

    def test_init_with_connection_string(
        self, mocker, mock_blob_service_client, monkeypatch
    ):
        """
        Tests that the BlobService initializes correctly with a connection string.
        """
        monkeypatch.setattr(
            blob_service.settings, "BLOB_CONNECTION_STRING", "test_conn_str"
        )
        monkeypatch.setattr(blob_service.settings, "BLOB_ENDPOINT", None)
        mocker.patch(
            "app.services.blob_service.BlobServiceClient.from_connection_string",
            return_value=mock_blob_service_client,
        )

        service = blob_service.BlobService()

        blob_service.BlobServiceClient.from_connection_string.assert_called_once_with(
            conn_str="test_conn_str"
        )
        assert service.client is not None

    def test_init_with_endpoint_and_credential(
        self, mocker, mock_blob_service_client, monkeypatch
    ):
        """
        Tests that the BlobService initializes correctly with an endpoint and credentials.
        """
        monkeypatch.setattr(blob_service.settings, "BLOB_CONNECTION_STRING", None)
        monkeypatch.setattr(blob_service.settings, "BLOB_ENDPOINT", "test_endpoint")
        mocker.patch("app.services.blob_service.DefaultAzureCredential")
        mocker.patch(
            "app.services.blob_service.BlobServiceClient",
            return_value=mock_blob_service_client,
        )

        service = blob_service.BlobService()

        blob_service.BlobServiceClient.assert_called_once()
        assert service.client is not None

    def test_init_no_config_raises_error(self, monkeypatch):
        """
        Tests that a ValueError is raised if no storage configuration is provided.
        """
        monkeypatch.setattr(blob_service.settings, "BLOB_CONNECTION_STRING", None)
        monkeypatch.setattr(blob_service.settings, "BLOB_ENDPOINT", None)
        with pytest.raises(ValueError, match="Storage configuration missing"):
            blob_service.BlobService()


# --- Tests for the public service methods ---


class TestBlobServiceMethods:
    """Tests for the public methods of the BlobService."""

    @pytest.fixture(autouse=True)
    def setup_service(self, mocker, mock_blob_service_client, monkeypatch):
        """
        Sets up the BlobService for testing.
        """
        monkeypatch.setattr(
            blob_service.settings, "BLOB_CONNECTION_STRING", "test_conn_str"
        )
        mocker.patch(
            "app.services.blob_service.BlobServiceClient.from_connection_string",
            return_value=mock_blob_service_client,
        )

        self.service = blob_service.BlobService()
        self.mock_container = self.service.client.get_container_client.return_value
        self.mock_blob = self.mock_container.get_blob_client.return_value

    @pytest.mark.asyncio
    async def test_write_blob_when_container_exists(self):
        """
        Tests writing a blob when the container already exists.
        """
        await self.service.write_blob("test-container", "test.txt", b"data")
        self.mock_container.get_container_properties.assert_awaited_once()
        self.mock_container.create_container.assert_not_awaited()
        self.mock_blob.upload_blob.assert_awaited_once_with(b"data", overwrite=True)

    @pytest.mark.asyncio
    async def test_write_blob_creates_container_if_not_found(self):
        """
        Tests that a container is created if it does not exist when writing a blob.
        """
        self.mock_container.get_container_properties.side_effect = (
            ResourceNotFoundError()
        )
        await self.service.write_blob("test-container", "test.txt", b"data")
        self.mock_container.get_container_properties.assert_awaited_once()
        self.mock_container.create_container.assert_awaited_once()
        self.mock_blob.upload_blob.assert_awaited_once_with(b"data", overwrite=True)

    @pytest.mark.asyncio
    async def test_get_blob_succeeds(self):
        """
        Tests successfully getting a blob.
        """
        data = await self.service.get_blob("test-container", "test.txt")
        assert data == b"test blob content"
        self.mock_blob.download_blob.assert_awaited_once()
        self.mock_blob.download_blob.return_value.readall.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_blob_raises_when_not_found(self):
        """
        Tests that getting a non-existent blob raises a ResourceNotFoundError.
        """
        self.mock_blob.download_blob.side_effect = ResourceNotFoundError()
        with pytest.raises(ResourceNotFoundError):
            await self.service.get_blob("test-container", "test.txt")

    @pytest.mark.asyncio
    async def test_delete_blob_succeeds(self):
        """
        Tests successfully deleting a blob.
        """
        await self.service.delete_blob("test-container", "test.txt")
        self.mock_blob.delete_blob.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_delete_blob_handles_not_found_gracefully(self):
        """
        Tests that deleting a non-existent blob does not raise an exception.
        """
        self.mock_blob.delete_blob.side_effect = ResourceNotFoundError()
        try:
            await self.service.delete_blob("test-container", "test.txt")
        except ResourceNotFoundError:
            pytest.fail("Deleting a non-existent blob should not raise an exception.")
