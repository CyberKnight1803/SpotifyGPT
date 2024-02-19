import os 

from fastapi import FastAPI, Request, Response
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from src.api import router as api_router
from src.spotify import router as spotify_router

from config import (
    HOST, PORT, 
    RESPONSE_TIME_LIMIT, 
)


# Create FastAPI app instance 
app = FastAPI()

# Cross-Origin Resource sharing
ALLOWED_ORIGINS = [
    "https://tanishabisht.github.io",  # Add more origins as needed
]

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # List of allowed origins
    allow_credentials=True,  # Whether to support cookies
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# handle CORS preflight requests
@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = "https://tanishabisht.github.io"
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response

# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = "https://tanishabisht.github.io"
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response



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