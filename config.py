import os 
from dotenv import load_dotenv

# Load keys
load_dotenv()

# Website 
BASE_URI = os.getenv("BASE_URI")

# OpenAI keys 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Spotify keys
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_AUTH_URL = os.getenv("SPOTIFY_AUTH_URL")
SPOTIFY_TOKEN_URL = os.getenv("SPOTIFY_TOKEN_URL")
SPOTIFY_BASE_URL = os.getenv("SPOTIFY_BASE_URL")
