from app.services.cosmos_service import CosmosService
# from app.services.blob_service import BlobService
from typing import Optional

cosmos_service = CosmosService()
# blob_service = BlobService()

def get_cosmos_service() -> Optional[CosmosService]:
    return cosmos_service

# def get_blob_service() -> Optional[BlobService]:
#     return blob_service