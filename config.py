import os 
from dotenv import load_dotenv

# Load keys
load_dotenv()

# Website 
BASE_URI = "http://localhost:8000"

# OpenAI keys 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Spotify keys
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/"
