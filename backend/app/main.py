from fastapi import FastAPI, Depends
import logging
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace, _logs

from app.routers import accounts_router, room_router, test_router
from app.dependencies import get_cosmos_service, get_blob_service
from app.services.cosmos_service import CosmosService
from app.services.blob_service import BlobService
from app.config import settings

# Need Azure Application Insights API key
if settings.APPLICATION_INSIGHTS_CONNECTION_STRING:
    configure_azure_monitor()

# Shutdown
@asynccontextmanager
async def lifespan(app: FastAPI, cosmos_service: CosmosService = Depends(get_cosmos_service), blob_service: BlobService = Depends(get_blob_service)):
    yield
    # Azure Clients
    if blob_service:
        await blob_service.close()
    if cosmos_service:
        await cosmos_service.close()
    # OpenTelemetry
    tracer_provider = trace.get_tracer_provider()
    if hasattr(tracer_provider, 'shutdown'):
        tracer_provider.shutdown()
    logger_provider = _logs.get_logger_provider()
    if hasattr(logger_provider, 'shutdown'):
        logger_provider.shutdown()

app = FastAPI(lifespan=lifespan)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app.include_router(accounts_router.router)
app.include_router(room_router.router)
app.include_router(test_router.router)

# Then mount the static files at the root
# app.mount("/", StaticFiles(directory="path/to/frontend/build", html=True), name="static")

@app.get("/")
def test():
    return {"Hello": "World"}