import logging
from typing import List, Dict, Any, Optional

from azure.storage.blob.aio import BlobServiceClient
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.identity.aio import DefaultAzureCredential

from app.config import settings

class BlobService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client: BlobServiceClient
        if settings.BLOB_CONNECTION_STRING:
            self.logger.info("Initializing Blob Service Client with Connection String")
            self.client = BlobServiceClient.from_connection_string(conn_str=settings.BLOB_CONNECTION_STRING)
        elif settings.BLOB_ENDPOINT:
            self.logger.info("Initializing Blob Service Client with Azure Credentials")
            credential = DefaultAzureCredential()
            self.client = BlobServiceClient(account_url=settings.BLOB_ENDPOINT, credential=credential)
        else:
            raise ValueError("Storage configuration missing. Set either BLOB_CONNECTION_STRING or BLOB_ENDPOINT")

        if not self.client:
            raise ConnectionError("Failed to connect to BlobServiceClient")
    
    async def close(self):
        self.logger.info("Closing Blob Storage client session")
        await self.client.close()
        
    async def write_blob(self, container_name: str, filename: str, blobstream: Any):
        if not container_name:
            raise ValueError("Container name cannot be empty")
        if not blobstream:
            raise ValueError("Blob content cannot be null")
        try:
            container_client = self.client.get_container_client(container_name)
            # Check if container exists
            try:
                await container_client.get_container_properties()
            except ResourceNotFoundError:
                await container_client.create_container()
                self.logger.info(f"Container '{container_name}' created.")
            
            blob_client = container_client.get_blob_client(filename)
            await blob_client.upload_blob(blobstream, overwrite=True)
            self.logger.info(f"Blob '{filename}' uploaded successfully to container '{container_name}'")
            
        except HttpResponseError as e:
            self.logger.error(f"Azure Storage request failed: {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during blob upload: {e}")
            raise
        
    async def delete_blob(self, container_name: str, filename: str):
        if not container_name:
            raise ValueError("Container name cannot be empty")
        if not filename:
            raise ValueError("Filename cannot be empty")
        try:
            container_client = self.client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(filename)
            await blob_client.delete_blob()
            self.logger.info(f"Blob '{filename}' deleted from container '{container_name}'")
        except ResourceNotFoundError:
            self.logger.warning(
                f"Attempted to delete blob '{filename}', but does not exist in container {container_name}")
        except Exception as e:
            self.logger.error(f"Unexpected error during blob upload: {e}")
            raise