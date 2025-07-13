from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import room_router

app = FastAPI()

# Mount the API router first
app.include_router(room_router.router)

# Then mount the static files at the root
app.mount("/", StaticFiles(directory="path/to/frontend/build", html=True), name="static")