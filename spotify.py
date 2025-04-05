# spotify.py
from dotenv import load_dotenv
import os
import base64
import requests
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {
        "Authorization": "Bearer " + token,
    }

def get_top_tracks(token, limit=10, time_range="short_term"):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = get_auth_header(token)
    params = {"limit": limit, "time_range": time_range}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Error fetching top tracks:", response.json())
        return []

    top_tracks = response.json()["items"]
    track_list = []
    for idx, track in enumerate(top_tracks):
        track_list.append({
            "rank": idx + 1,
            "name": track["name"],
            "artists": ", ".join([artist["name"] for artist in track["artists"]]),
            "id": track["id"],
            "uri": track["uri"]
        })
    return track_list

def get_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    tracks = []
    params = {"limit": 100, "offset": 0}
    while True:
        result = requests.get(url, headers=headers, params=params)
        json_result = json.loads(result.content)
        items = json_result.get("items", [])
        for item in items:
            if "track" in item:
                track = item["track"]["name"]
                artists = ", ".join(artist["name"] for artist in item["track"]["artists"])
                tracks.append(f"{track} - {artists}")
        if json_result.get("next"):
            params["offset"] += 100
        else:
            break
    return tracks