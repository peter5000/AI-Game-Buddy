import logging
from typing import Any, Optional

from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError
from azure.identity.aio import DefaultAzureCredential
from fastapi import HTTPException, status

from app.config import settings

logger = logging.getLogger(__name__)


class CosmosService:
    """
    A service for interacting with Azure Cosmos DB.

    This class provides methods for performing CRUD operations on items in
    Cosmos DB containers. It handles the connection to Cosmos DB using either
    a connection string or an endpoint with Azure credentials.
    """

    def __init__(self):
        """
        Initializes the CosmosService.

        The client is initialized using either a connection string or an endpoint
        with Azure credentials, based on the application settings. It also
        initializes clients for the 'users' and 'rooms' containers.

        Raises:
            ValueError: If the database configuration is missing.
            ConnectionError: If the connection to the CosmosClient fails.
        """
        self.client: Optional[CosmosClient] = None

        if settings.COSMOS_CONNECTION_STRING:
            logger.info("Initializing Cosmos Service Client with Connection String")
            self.client = CosmosClient.from_connection_string(
                conn_str=settings.COSMOS_CONNECTION_STRING
            )
        elif settings.COSMOS_ENDPOINT:
            # Use managed identity if no connection string
            logger.info("Initializing Cosmos Service Client with Azure Credentials")
            credential = DefaultAzureCredential()
            self.client = CosmosClient(
                url=settings.COSMOS_ENDPOINT, credential=credential
            )
        else:
            raise ValueError(
                "Database configuration missing. Set either COSMOS_CONNECTION_STRING or COSMOS_ENDPOINT"
            )

        if not self.client:
            raise ConnectionError("Failed to connect to CosmosClient")

        db_client = self.client.get_database_client(settings.COSMOS_DATABASE_NAME)
        self.users_container_client = db_client.get_container_client("users")
        self.rooms_container_client = db_client.get_container_client("rooms")

    async def close(self):
        """Closes the Cosmos DB client session."""
        logger.info("Closing Cosmos client session")
        await self.client.close()

    def get_container(self, container_type: str):
        """
        Gets the container client for a specified container type.

        Args:
            container_type (str): The type of container ('users' or 'rooms').

        Returns:
            The container client for the specified container type.

        Raises:
            ValueError: If the container type is invalid.
        """
        if container_type == "users":
            return self.users_container_client
        elif container_type == "rooms":
            return self.rooms_container_client
        else:
            raise ValueError(f"Container type '{container_type}' does not exist")

    # Database access functions
    async def add_item(self, item: dict[str, Any], container_type: str):
        """
        Adds an item to a specified container.

        Args:
            item (dict[str, Any]): The item to add.
            container_type (str): The type of container.

        Raises:
            ValueError: If the item is invalid.
            HTTPException: If a database error occurs.
        """
        if not item:
            raise ValueError("Invalid Item")

        container = self.get_container(container_type)
        logger.info(f"Adding item to container '{container.id}': '{item.get('id')}'")
        try:
            await container.create_item(body=item)
        except CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error adding item '{item.get('id')}': {e.message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred during the patch operation",
            )
        except Exception as e:
            logger.error(
                f"Failed to add item '{item.get('id')}' to '{container.id}': {e}"
            )
            raise

    async def get_item(self, item_id: str, partition_key: str, container_type: str):
        """
        Gets an item from a specified container.

        Args:
            item_id (str): The ID of the item to get.
            partition_key (str): The partition key of the item.
            container_type (str): The type of container.

        Returns:
            The item if found, otherwise None.

        Raises:
            ValueError: If the item ID or partition key is empty.
            HTTPException: If a database error occurs.
        """
        if not item_id or not partition_key:
            raise ValueError("Item ID and partition key cannot be empty")

        container = self.get_container(container_type)
        logger.info(
            f"Geting item from container '{container.id}' with item id '{item_id}' and partition key '{partition_key}'"
        )
        try:
            item = await container.read_item(item=item_id, partition_key=partition_key)
            return item
        except CosmosResourceNotFoundError:
            logger.warning(
                f"Item '{item_id}' with partition key '{partition_key}' not found in container '{container.id}'"
            )
            return None
        except CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error getting item '{item_id}': {e.message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred during the get operation",
            )
        except Exception as e:
            logger.error(
                f"Failed to get item '{item_id}' with partition key '{partition_key}' from '{container.id}': {e}"
            )
            raise

    # Getting items using a SQL Query
    async def get_items_by_query(
        self,
        query: str,
        container_type: str,
        parameters: Optional[list[dict[str, Any]]] = None,
    ) -> list[dict[str, Any]]:
        """
        Gets items from a specified container using a SQL query.

        Args:
            query (str): The SQL query to execute.
            container_type (str): The type of container.
            parameters (Optional[list[dict[str, Any]]], optional): The parameters for the query. Defaults to None.

        Returns:
            list[dict[str, Any]]: A list of items returned by the query.

        Raises:
            ValueError: If the query string is empty.
            HTTPException: If a database error occurs.
        """
        if not query:
            raise ValueError("Query string cannot be empty")

        container = self.get_container(container_type)
        logger.info(f"Querying items in container '{container.id}': {query}")
        try:
            items = [
                item
                async for item in container.query_items(
                    query=query, parameters=parameters
                )
            ]
            logger.info(f"Query returned {len(items)} items")
            return items
        except CosmosHttpResponseError as e:
            logger.error(
                f"Cosmos DB query failed with status {e.status_code}: {e.message}"
            )
            if e.status_code == 400:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid query syntax: {e.message}",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"A database error occurred while executing the query: {query}",
                )
        except Exception as e:
            logger.error(f"Failed to execute query {query}: {e}")
            raise

    async def update_item(self, item: dict[str, Any], container_type: str):
        """
        Updates an item in a specified container.

        Args:
            item (dict[str, Any]): The item to update.
            container_type (str): The type of container.

        Raises:
            ValueError: If the item is invalid.
            HTTPException: If the item is not found or a database error occurs.
        """
        if not item:
            raise ValueError("Invalid Item")

        container = self.get_container(container_type)
        logger.info(f"Updating item to container '{container.id}': '{item.get('id')}'")
        try:
            await container.upsert_item(body=item)
        except CosmosResourceNotFoundError:
            logger.warning(
                f"Item '{item.get('id')}' not found in container '{container.id}' for patching"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id '{item.get('id')}' not found",
            )
        except CosmosHttpResponseError as e:
            logger.error(
                f"Cosmos DB error updating item '{item.get('id')}': {e.message}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred during the patch operation",
            )
        except Exception as e:
            logger.error(
                f"Failed to update item '{item.get('id')}' to '{container.id}': {e}"
            )
            raise

    async def patch_item(
        self,
        item_id: str,
        partition_key: str,
        patch_operations: dict[str, Any],
        container_type: str,
    ):
        """
        Patches an item in a specified container.

        Args:
            item_id (str): The ID of the item to patch.
            partition_key (str): The partition key of the item.
            patch_operations (dict[str, Any]): The patch operations to perform.
            container_type (str): The type of container.

        Raises:
            ValueError: If the item ID or partition key is empty.
            HTTPException: If the item is not found or a database error occurs.
        """
        if not item_id or not partition_key:
            raise ValueError("Item ID and partition key cannot be empty")

        container = self.get_container(container_type)
        logger.info(f"Patching item '{item_id}' from container '{container.id}")
        try:
            await container.patch_item(
                item=item_id,
                partition_key=partition_key,
                patch_operations=patch_operations,
            )
        except CosmosResourceNotFoundError:
            logger.warning(
                f"Item '{item_id}' not found in container '{container.id}' for patching"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id '{item_id}' not found",
            )
        except CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error patching item '{item_id}': {e.message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred during the patch operation",
            )
        except Exception as e:
            logger.critical(
                f"An unexpected error occurred while patching item '{item_id}': {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected internal error occurred",
            )

    async def delete_item(self, item_id: str, partition_key: str, container_type: str):
        """
        Deletes an item from a specified container.

        Args:
            item_id (str): The ID of the item to delete.
            partition_key (str): The partition key of the item.
            container_type (str): The type of container.

        Raises:
            ValueError: If the item ID or partition key is empty.
            HTTPException: If the item is not found or a database error occurs.
        """
        if not item_id or not partition_key:
            raise ValueError("Item ID and partition key cannot be empty")

        container = self.get_container(container_type)
        logger.info(
            f"Deleting item from container '{container.id}': '{item_id}' with partition key '{partition_key}'"
        )
        try:
            await container.delete_item(item=item_id, partition_key=partition_key)
        except CosmosResourceNotFoundError:
            logger.warning(
                f"Item '{item_id}' not found in container '{container.id}' for deleting"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id '{item_id}' not found",
            )
        except CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error deleting item '{item_id}': {e.message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred during the delete operation",
            )
        except Exception as e:
            logger.critical(
                f"An unexpected error occurred while patching item '{item_id}': {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected internal error occurred",
            )
