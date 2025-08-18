import asyncio
import logging
from contextlib import asynccontextmanager
try:
    from azure.monitor.opentelemetry import configure_azure_monitor
    from opentelemetry import trace, _logs
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

from app.routers import accounts_router, room_router, test_router, game_router
try:
    from app.dependencies import cosmos_service, blob_service
    DEPS_AVAILABLE = True
except ImportError:
    cosmos_service = None
    blob_service = None
    DEPS_AVAILABLE = False

if AZURE_AVAILABLE and settings.APPLICATIONINSIGHTS_CONNECTION_STRING:
    configure_azure_monitor()


# Shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    # Start up
    # Start the Redis subscribe method as a background task
    subscribe_task = asyncio.create_task(redis_listener())

    yield
    # Shutdown
    subscribe_task.cancel()
    try:
        await subscribe_task
    except asyncio.CancelledError:
        pass

    # Database/Storage Clients
    await get_blob_service().close()
    await get_cosmos_service().close()
    await get_redis_service().close()

    # OpenTelemetry
    if AZURE_AVAILABLE:
        tracer_provider = trace.get_tracer_provider()
        if hasattr(tracer_provider, 'shutdown'):
            tracer_provider.shutdown()
        logger_provider = _logs.get_logger_provider()
        if hasattr(logger_provider, 'shutdown'):
            logger_provider.shutdown()


app = FastAPI(lifespan=lifespan)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
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
