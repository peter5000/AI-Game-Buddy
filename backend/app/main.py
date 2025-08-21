from fastapi import FastAPI
from app.config import settings
import logging
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace, _logs

from app.routers import accounts_router, room_router, test_router, game_router, websocket_router
from app.dependencies import get_cosmos_service, get_blob_service, get_redis_service

if settings.APPLICATIONINSIGHTS_CONNECTION_STRING:
    configure_azure_monitor()

# Shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Azure Clients
    if get_blob_service():
        await get_blob_service().close()
    if get_cosmos_service():
        await get_cosmos_service().close()
    if get_redis_service():
        await get_redis_service().close()
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

FastAPIInstrumentor.instrument_app(app)

app.include_router(accounts_router.router)
app.include_router(room_router.router)
app.include_router(test_router.router)
app.include_router(game_router.router)
app.include_router(websocket_router.router)

# Then mount the static files at the root
# app.mount("/", StaticFiles(directory="path/to/frontend/build", html=True), name="static")

@app.get("/")
def test():
    return {"Hello": "World"}