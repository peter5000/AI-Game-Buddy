from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import router  # Fictional router import

app = FastAPI()

# Mount the API router first
app.include_router(router, prefix="/api")

# Then mount the static files at the root
app.mount("/", StaticFiles(directory="path/to/frontend/build", html=True), name="static")