import os
import base64
import requests
from urllib.parse import urlencode

from pydantic import BaseModel 
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, JSONResponse

from src.openai import get_gpt4_suggestions, Query
from src.spotify import get_spotify_track, create_spotify_playlist, add_songs, SpotifyPlaylist

# Create router 
router = APIRouter(
    prefix="/api"
)

@router.get("/api-health-check")
async def api_health_check():
    """
        Sample API endpoint to check if this router works or not
    """
    
    return {
        "message": "Spotify API is connected successfully"
    }

@router.post("/suggestions")
async def get_suggestions(query: Query):
    """
        Get GPT suggestions of songs and get song track IDs and other details using spotify web api
    """

    # Get GPT-4 suggestions
    suggestions = get_gpt4_suggestions(query.user_prompt, query.num_suggestions) 

    # Get track IDs and external links
    tracks = []
    for suggestion in suggestions:
        track_name = suggestion['title']
        artist_name = suggestion['artist']

        # Get track data from spotify search
        track_data = get_spotify_track(track_name, artist_name, query.access_token) 
        tracks.append(track_data)
    
    return JSONResponse(content=jsonable_encoder(tracks))

# Create playlist -
@router.post("/create-playlist")
async def create_playlist(playlist: SpotifyPlaylist):
    """
        Create plaulist on spotify for user
    """ 
    
    # Create playlist
    playlist_details = create_spotify_playlist(
        user_id=playlist.user_id, 
        playlist_name=playlist.name, 
        access_token=playlist.access_token
    )

    # Add songs to playlist
    snapshot_id = add_songs(
        playlist_id=playlist_details['id'], 
        track_ids=playlist.track_ids,
        access_token=playlist.access_token
    )

    return playlist_details['link']