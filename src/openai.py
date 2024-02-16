import os 
import json
from openai import OpenAI
from pydantic import BaseModel

from config import (
    OPENAI_API_KEY, 
    GPT_MODEL
)

# Get OpenAI Client 
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# Query 
class Query(BaseModel):
    user_prompt: str            # User prompt got from the free-text search field
    num_suggestions: int        # Number of tracks required 
    access_token: str           # Access token generated by user to access spotify web api



def get_gpt4_suggestions(user_prompt: str, num_suggestions: int):
    """
        Get GPT-4 suggestions
    """ 
    
    # Prompt to tell who GPT-4 role plays
    system_prompt = """
    You are the best Spotify song recommender this world has ever seen. 
    You accurately understand the user's feelings and desire to hear the type of songs from his request and you suggest the best songs which could be turned into the best playlist.
    You only recommend songs available on spotify.
    """

    # Prompt to get suggestions
    prompt = f"""
    Suggest {num_suggestions} songs based on the following user's prompt: 

    {user_prompt}

    Note: Follow the below rules strictly to generate the output
    1. You are to suggest only track names and first artist 
    2. The output should strictly be JSON parsable. 

    Example: Output for 2 songs recommended by you should look like a list of 2 dictionaries, where each dictionary will have two key value pairs i.e. "title": "song_name", "artist": "artist_name"
    """

    # Get reponse from gpt-4
    response = openai_client.chat.completions.create(
        model=GPT_MODEL, 
        max_tokens=2000,
        response_format={
            'type': 'json_object'           # GPT-4 Turbo model can set JSON object as output format
        },
        messages=[
            {
                "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text", 
                        "text": prompt
                    }
                ]
            }
        ]
    )

    # Get dictionary format
    suggestions = json.loads(response.choices[0].message.content)
    return suggestions['songs']
    

