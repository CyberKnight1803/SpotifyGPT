import os 

from fastapi import FastAPI
import uvicorn

from src.api import router as api_router
from src.spotify import router as spotify_router

from config import (
    HOST, 
    PORT
)


# Create FastAPI app instance 
app = FastAPI()

# Add Routers 
app.include_router(api_router)
app.include_router(spotify_router)


@app.get("/")
async def home_page():
    return "HOME PAGE"


if __name__ == "__main__":

    # Uvicorn 
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)

    # Test cloud