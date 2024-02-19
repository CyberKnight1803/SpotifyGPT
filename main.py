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

# CORS middleware

origins = [
    'http://localhost:3000', 
    'http://0.0.0.0:3000', 
    '*'
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"], 
        allow_headers=["*"], 
        allow_credentials=True
    )
]

# Create FastAPI app instance 
app = FastAPI(middleware=middleware)

# Cross-Origin Resource sharing
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_methods=["*"], 
#     allow_headers=["*"], 
#     allow_credentials=True, 
#     expose_headers=["Access-Control-Allow-Origin"],
#     max_age=RESPONSE_TIME_LIMIT
# )

# Salt to your taste
ALLOWED_ORIGINS = '*'    # or 'foo.com', etc.

# handle CORS preflight requests
@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response

# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
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