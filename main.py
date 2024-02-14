import os 

from fastapi import FastAPI
import uvicorn

from src.openai import router as openai_router
from src.spotify import router as spotify_router

from config import (
    HOST, 
    PORT
)


# Create FastAPI app instance 
app = FastAPI()

# Add Routers 
app.include_router(openai_router)
app.include_router(spotify_router)


@app.get("/")
async def home_page():
    return "HOME PAGE"

@app.get("/api-health-check")
async def api_health_check():
    return {
        "message": "FastAPI is working correctly"
    } 


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)