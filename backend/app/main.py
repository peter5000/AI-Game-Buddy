from fastapi import FastAPI
import logging
from fastapi.staticfiles import StaticFiles
from app.routers import room_router, test_router

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Need Azure Application Insights API key
# configure_azure_monitor()

app = FastAPI()

# Setting up logging configuration
FastAPIInstrumentor.instrument_app(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mount the API router first
app.include_router(room_router.router)
app.include_router(test_router.router)

# Then mount the static files at the root
# app.mount("/", StaticFiles(directory="path/to/frontend/build", html=True), name="static")

@app.get("/")
def test():
    return {"Hello": "World"}