import os 
from dotenv import load_dotenv

# Load keys
load_dotenv()

# Website 
HOST = '0.0.0.0'
PORT = 8000

BASE_URI = os.getenv("BASE_URI")

# OpenAI keys 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_MODEL = "gpt-4-0125-preview"

# Spotify keys
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1"
