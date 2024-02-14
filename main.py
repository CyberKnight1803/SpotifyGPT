import os 

from fastapi import FastAPI
from dotenv import load_dotenv

from src.openai import router as openai_router
from src.spotify import router as spotify_router


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
