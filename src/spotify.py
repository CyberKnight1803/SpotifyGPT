import base64
import json
import requests
from typing import List
from urllib.parse import urlencode
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse

from config import (
    BASE_URI,
    SPOTIFY_CLIENT_ID, 
    SPOTIFY_CLIENT_SECRET, 
    SPOTIFY_AUTH_URL, 
    SPOTIFY_TOKEN_URL,
    SPOTIFY_BASE_URL
)

# REDIRECT_URI = BASE_URI + "/spotify/callback"
REDIRECT_URI = "https://tanishabisht.github.io/spotifygpt-frontend/"
SEARCH_TYPE = "track"
SEARCH_LIMIT = 1

# Create router 
router = APIRouter(
    prefix="/spotify"
)

@router.get("/api-health-check")
async def api_health_check():
    """
        Sample API endpoint to check if this router works or not
    """
    
    return {
        "message": "Spotify API is connected successfully"
    }

@router.get("/login")
async def spotify_login(response: Response):
    """
        User Spotify login
    """

    # Scope: Need access to create a new private playlist
    scope = "user-read-private user-read-email playlist-modify-private"

    # Params
    params = {
        "response_type": "code", 
        "client_id": SPOTIFY_CLIENT_ID, 
        "scope": scope, 
        "redirect_uri": REDIRECT_URI, 
    }

    # Redirect to spotify auth
    response = RedirectResponse(
        url=SPOTIFY_AUTH_URL + '?' + urlencode(params)
    )

    return response

@router.options("/callback")
@router.get('/callback')
async def callback(request: Request, response: Response):

    # Access query params
    code = request.query_params["code"]


    # base64 encode client_id and client_secret
    request_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET
    encoded_bytes = base64.b64encode(request_string.encode("utf-8"))
    encoded_string = str(encoded_bytes, "utf-8")

    # Feed them as header
    header = {"Authorization": "Basic " + encoded_string}

    # Payload
    form_data = {
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    # Post request to get spotify api access token
    api_response = requests.post(SPOTIFY_TOKEN_URL, data=form_data, headers=header)
    if api_response.status_code == 200:
        data = api_response.json()

        url = SPOTIFY_BASE_URL + "/me"
        headers = {
            "Authorization": f"Authorization: Bearer {data['access_token']}" 
        }

        user_data_response = requests.get(url, headers=headers)

        if user_data_response.status_code == 200:
            user_data = user_data_response.json()
            data.update({'name': user_data['display_name']})
            data.update({'email': user_data['email']})
            data.update({'user_id': user_data['id']})
            data.update({'user_profile': user_data['external_urls']['spotify']})
            return data
        
        else:
            HTTPException(status_code=user_data_response.status_code, detail="Error in getting User details")


    else:
        # State value is not same => Stop the process and throw error 
        raise HTTPException(status_code=400, detail="Error in getting Spotify token")    



class SpotifyPlaylist(BaseModel):
    user_id: str
    name: str 
    track_ids: List[str]
    access_token: str


def get_spotify_track(
        track_name: str, 
        artist_name: str, 
        access_token: str, 
        type: str = SEARCH_TYPE, 
        limit: int = SEARCH_LIMIT
    ):

    params = {
        "q": f"{track_name}%{artist_name}", 
        "type": type, 
        "limit": limit
    }

    headers = {
        "Authorization": f"Authorization: Bearer {access_token}"
    }

    url = SPOTIFY_BASE_URL + "/search" + "?" + urlencode(params)

    response = requests.get(url, headers=headers)
    track_details = response.json()

    # Process artists 
    artists = []
    for artist in track_details['tracks']['items'][0]['artists']:
        artists.append(artist['name'])

    track_data = {
        "id": track_details['tracks']['items'][0]['id'], 
        "name": track_details['tracks']['items'][0]['name'],
        "artists": artists,
        'external_url': track_details['tracks']['items'][0]['external_urls']['spotify'], 
        'images': track_details['tracks']['items'][0]['album']['images']
    }

    return track_data    


def create_spotify_playlist(
        user_id: str,
        playlist_name: str, 
        access_token: str
    ):
    
    data = {
        "name": playlist_name, 
        "public": False
    } 

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Authorization: Bearer {access_token}"
    }

    url = SPOTIFY_BASE_URL + f"/users/{user_id}/playlists"

    response = requests.post(url, data=json.dumps(data), headers=headers)
    playlist_data = response.json()

    
    playlist = {
        'id': playlist_data['id'], 
        'link': playlist_data['external_urls']['spotify']
    }

    return playlist

def add_songs(
        playlist_id: str, 
        track_ids: List[str], 
        access_token: str
    ):

    uris = []
    for track_id in track_ids:
        uris.append(f"spotify:track:{track_id}")
    
    data = {
        "uris": uris, 
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Authorization: Bearer {access_token}"
    }

    url = SPOTIFY_BASE_URL + f"/playlists/{playlist_id}/tracks"

    snapshot_id = requests.post(url, data=json.dumps(data), headers=headers)
    return snapshot_id 


