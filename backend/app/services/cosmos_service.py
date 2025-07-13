import logging
from typing import List, Dict, Any

from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from azure.identity.aio import DefaultAzureCredential

from config import settings

# Initialization
COSMOS_CONNECTION_STRING = settings.COSMOS_CONNECTION_STRING
COSMOS_ENDPOINT = settings.COSMOS_ENDPOINT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client = None
if COSMOS_CONNECTION_STRING:
    client = CosmosClient.from_connection_string(conn_str=COSMOS_CONNECTION_STRING)
elif COSMOS_ENDPOINT:
    # use managed identity if no connection string
    credential = DefaultAzureCredential()
    client = CosmosClient(url=COSMOS_ENDPOINT, credential=credential)
else:
    raise ValueError("Database configuration missing. Set either COSMOS_CONNECTION_STRING or COSMOS_ENDPOINT")

COSMOS_DATABASE_NAME = settings.COSMOS_DATABASE_NAME
db_client = client.get_database_client(COSMOS_DATABASE_NAME)
users_container_client = db_client.get_container_client("users")

def get_container(container_type: str):
    if container_type == "users":
        return users_container_client
    else:
        raise ValueError(f"Container type {container_type} does not exist")
    
# Database access functions
async def add_item(item: Dict[str, Any], container_type: str):
    if not item:
        raise ValueError("Invalid Item")
    
    container = get_container(container_type)
    logger.info(f"Adding item to container {container.id}: {item.get('id')}")
    try:
        await container.create_item(body=item)
    except Exception as e:
        logger.error(f"Failed to add item {item.get('id')} to {container.id}: {e}")
        raise

async def get_item(item_id: str, container_type: str, partition_key: str):
    if not item_id or not partition_key:
        raise ValueError("Item ID and partition key cannot be empty")
    
    container = get_container(container_type)
    logger.info(f"Geting item from container {container.id} with item id {item_id} and partition key {partition_key}")
    try:
        item = await container.read_item(item=item_id, partition_key=partition_key)
        return item
    except CosmosResourceNotFoundError:
        logger.warning(f"Item '{item_id}' with partition key {partition_key} not found in container {container.id}")
        return None
    except Exception as e:
        logger.error(f"Failed to get item {item_id} with partition key {partition_key} from {container.id}: {e}")
        raise

# Getting items using a NoSQL Query
async def get_items_by_query(query: str, container_type: str) -> List[Dict[str, Any]]:
    if not query:
        raise ValueError("Query string cannot be empty")
    
    container = get_container(container_type)
    logger.info(f"Querying items in container {container.id}: {query}")
    try:
        items = [item async for item in container.query_items(query=query, enable_cross_partition_query=True)]
        logger.info(f"Query returned {len(items)} items")
        return items
    except Exception as e:
        logger.error(f"Failed to execute query {query}: {e}")
        raise

async def update_item(item: Dict[str, Any], container_type: str):
    if not item:
        raise ValueError("Invalid Item")
    
    container = get_container(container_type)
    logger.info(f"Updating item to container {container.id}: {item.get('id')}")
    try:
        await container.upsert_item(body=item)
    except Exception as e:
        logger.error(f"Failed to update item {item.get('id')} to {container.id}: {e}")
        raise
    
async def delete_item(item_id: str, partition_key: str, container_type: str):
    if not item_id or not partition_key:
        raise ValueError("Item ID and partition key cannot be empty")
    
    container = get_container(container_type)
    logger.info(f"Deleting item from container {container.id}: {item_id} with partition key {partition_key}")
    try:
        await container.delete_item(item=item_id, partition_key=partition_key)
    except Exception as e:
        logger.error(f"Failed to delete item {item_id} with partition key {partition_key} from {container.id}: {e}")
        raise