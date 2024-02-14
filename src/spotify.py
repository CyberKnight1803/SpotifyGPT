import os
import base64
import requests
from urllib.parse import urlencode

from pydantic import BaseModel 
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse

from utils import (
    generate_random_string
)

from config import (
    BASE_URI,
    SPOTIFY_CLIENT_ID, 
    SPOTIFY_CLIENT_SECRET, 
    SPOTIFY_AUTH_URL, 
    SPOTIFY_TOKEN_URL,
    SPOTIFY_BASE_URL
)

STATE_KEY = "spotify_auth_state"
REDIRECT_URI = BASE_URI + "/spotify/callback"


# Client Authentication 
class SpotifyClientAuth(BaseModel):
    client_id: str 
    client_secret: str


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
    
    # Generate random state 
    state = generate_random_string(10)

    # Scope: Need access to create a new private playlist
    scope = "user-read-private user-read-email playlist-modify-private"

    # Params
    params = {
        "response_type": "code", 
        "client_id": SPOTIFY_CLIENT_ID, 
        "scope": scope, 
        "redirect_uri": REDIRECT_URI, 
        "state": state
    }

    # Redirect to spotify auth
    response = RedirectResponse(
        url=SPOTIFY_AUTH_URL + '?' + urlencode(params)
    )

    # Set cookie to check if state value remains unchanged in callback
    response.set_cookie(key=STATE_KEY, value=state)
    return response

@router.get('/callback')
async def callback(request: Request, response: Response):

    # Access query params
    code = request.query_params["code"]
    state = request.query_params["state"]
    stored_state = request.cookies.get(STATE_KEY)

    # If state value has changed, stop the flow and throw error
    if state is None or state != stored_state:
        raise HTTPException(status_code=400, detail="State mismatch")
    
    else:
        # Delete coookie
        response.delete_cookie(STATE_KEY, path="/", domain=None)

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
            return data

        else:
            # State value is not same => Stop the process and throw error 
            raise HTTPException(status_code=400, detail="Error in getting Spotify token")    


@router.post("/api/search")
async def search_spotify():
    pass 