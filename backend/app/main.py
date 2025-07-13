from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import room_router, test_router

app = FastAPI()

# Mount the API router first
app.include_router(room_router.router)
app.include_router(test_router.router)

# Then mount the static files at the root
# app.mount("/", StaticFiles(directory="path/to/frontend/build", html=True), name="static")

@app.get("/")
def test():
    return {"Hello": "World"}