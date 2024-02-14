import os 
from fastapi import APIRouter
from config import (
    OPENAI_API_KEY
)

# Create router 
router = APIRouter(
    prefix="/openai"
)


@router.get("/api-health-check")
async def api_health_check():
    return {
        "message": "OpenAI API is connected successfully"
    }