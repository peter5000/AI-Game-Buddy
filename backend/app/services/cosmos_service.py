import logging
from typing import List, Dict, Any, Optional

from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from azure.identity.aio import DefaultAzureCredential

from app.config import settings

class CosmosService:
    def __init__(self):
        self.logger = logging.getLogger("CosmosService")
        self.client: Optional[CosmosClient] = None

        if settings.COSMOS_CONNECTION_STRING:
            self.logger.info("Initializing Cosmos Service Client with Connection String")
            self.client = CosmosClient.from_connection_string(conn_str=settings.COSMOS_CONNECTION_STRING)
        elif settings.COSMOS_ENDPOINT:
            # Use managed identity if no connection string
            self.logger.info("Initializing Cosmos Service Client with Azure Credentials")
            credential = DefaultAzureCredential()
            self.client = CosmosClient(url=settings.COSMOS_ENDPOINT, credential=credential)
        else:
            raise ValueError("Database configuration missing. Set either COSMOS_CONNECTION_STRING or COSMOS_ENDPOINT")

        if not self.client:
            raise ConnectionError("Failed to connect to CosmosClient")

        db_client = self.client.get_database_client(settings.COSMOS_DATABASE_NAME)
        self.users_container_client = db_client.get_container_client("users")
        # self.games_container_client = db_client.get_container_client("games")

    async def close(self):
        self.logger.info("Closing Cosmos client session")
        await self.client.close()

    def get_container(self, container_type: str):
        if container_type == "users":
            return self.users_container_client
        # elif container_type == "games":
        #     return self.games_container_client
        else:
            raise ValueError(f"Container type '{container_type}' does not exist")

    # Database access functions
    async def add_item(self, item: Dict[str, Any], container_type: str):
        if not item:
            raise ValueError("Invalid Item")

        container = self.get_container(container_type)
        self.logger.info(f"Adding item to container '{container.id}': '{item.get('id')}'")
        try:
            await container.create_item(body=item)
        except Exception as e:
            self.logger.error(f"Failed to add item '{item.get('id')}' to '{container.id}': {e}")
            raise

    async def get_item(self, item_id: str, container_type: str, partition_key: str):
        if not item_id or not partition_key:
            raise ValueError("Item ID and partition key cannot be empty")

        container = self.get_container(container_type)
        self.logger.info(f"Geting item from container '{container.id}' with item id '{item_id}' and partition key '{partition_key}'")
        try:
            item = await container.read_item(item=item_id, partition_key=partition_key)
            return item
        except CosmosResourceNotFoundError:
            self.logger.warning(f"Item '{item_id}' with partition key '{partition_key}' not found in container '{container.id}'")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get item '{item_id}' with partition key '{partition_key}' from '{container.id}': {e}")
            raise

    # Getting items using a SQL Query
    async def get_items_by_query(self, query: str, container_type: str, parameters: Optional[List[dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        if not query:
            raise ValueError("Query string cannot be empty")

        container = self.get_container(container_type)
        self.logger.info(f"Querying items in container '{container.id}': {query}")
        try:
            items = [item async for item in container.query_items(query=query, parameters=parameters)]
            self.logger.info(f"Query returned {len(items)} items")
            return items
        except Exception as e:
            self.logger.error(f"Failed to execute query {query}: {e}")
            raise

    async def update_item(self, item: Dict[str, Any], container_type: str):
        if not item:
            raise ValueError("Invalid Item")

        container = self.get_container(container_type)
        self.logger.info(f"Updating item to container '{container.id}': '{item.get('id')}'")
        try:
            await container.upsert_item(body=item)
        except Exception as e:
            self.logger.error(f"Failed to update item '{item.get('id')}' to '{container.id}': {e}")
            raise

    async def delete_item(self, item_id: str, partition_key: str, container_type: str):
        if not item_id or not partition_key:
            raise ValueError("Item ID and partition key cannot be empty")

        container = self.get_container(container_type)
        self.logger.info(f"Deleting item from container '{container.id}': '{item_id}' with partition key '{partition_key}'")
        try:
            await container.delete_item(item=item_id, partition_key=partition_key)
        except Exception as e:
            self.logger.error(f"Failed to delete item '{item_id}' with partition key '{partition_key}' from '{container.id}': {e}")
            raise