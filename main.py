from dotenv import load_dotenv
import os
import base64
import requests
from requests import post, get
import json
from datetime import datetime
import random
from collections import Counter

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print(client_id, client_secret)

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_top_tracks(token, limit=10, time_range = "short_term"):
    url = f"https://api.spotify.com/v1/me/top/tracks"
    headers = get_auth_header(token)
    params = {"limit": limit, "time_range": time_range}

    response = requests.get(url, headers = headers, params = params)

    if response.status_code != 200:
        print("Error fetching top tracks:", response.json())
        return []

    top_tracks = response.json()["items"]

    track_list = []
    for idx, track in enumerate(top_tracks):
        track_list.append({"rank": idx + 1, "name": track["name"], "artists": ", ".join([artist["name"] for artist in track["artists"]]), "id": track["id"], "uri": track["uri"]})
    return track_list
#
# def search_for_artist(token, artist_name):
#     url = "https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     query = f"?q={artist_name}&type=artist&limit=1"
#
#     query_url = url + query
#     result = get(query_url, headers=headers)
#     json_result = json.loads(result.content)["artists"]["items"]
#     if len(json_result) == 0:
#         print("Invalid")
#         return None
#
#     return json_result[0]
#
# def get_songs_by_artist(token, artist_id):
#     url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
#     headers = get_auth_header(token)
#     result = get(url, headers = headers)
#     json_result = json.loads(result.content)["tracks"]
#     return json_result
#

def get_random_number(min_value: int, max_value: int) -> int:
    """
    Fetches a random number from Random.org API.
    """
    api_key = "cb225b32-34a8-4a43-81af-879d58b5bd62"
    url = "https://api.random.org/json-rpc/4/invoke"

    # Payload for the Random.org JSON-RPC API
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": api_key,
            "n": 1,
            "min": min_value,
            "max": max_value,
            "replacement": True
        },
        "id": 42
    }

    # Make the request
    response = requests.post(url, json=payload)
    data = response.json()

    # Extract and return the random number
    return data["result"]["random"]["data"][0]


def get_ordinal_suffix(day: int) -> str:
    """
    Returns the ordinal suffix for a given day.
    """
    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return suffix

def get_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    tracks = []
    params = {
        "limit": 100,
        "offset": 0
    }
    while True:
        result = get(url, headers=headers, params=params)
        json_result = json.loads(result.content)

        items = json_result.get("items", [])
        for item in items:
            if "track" in item:
                track = item["track"]["name"]
                artists = ", ".join(artist["name"] for artist in item["track"]["artists"])
                tracks.append(f"{track} - {artists}")
        #tracks.extend([item["track"]["name"] for item in items if "track" in item])

        if json_result.get("next"):
            params["offset"] += 100
        else:
            break


    #tracks = [item["track"]["name"] for item in items if "track" in item]
    return tracks



today = datetime.now()

month = today.strftime("%B")
days = today.day
day_w_suffix = f"{days}{get_ordinal_suffix(days)}"
year = today.year


# Labeling token as getting the token
access_token = get_token()


# # Vibropix
# playlist_tracks = get_playlist(token, "21QjFtnTBkpVF1D1knEMBI")

# # Symphonaze
# playlist_tracks = get_playlist(token, "1Sr3Ry9hj2qrARewyFyKxY")

# # True Chill
# playlist_tracks = get_playlist(token, "3V21X4QHA7px8Ph4omNRVh")

# # Test Playlist
# playlist_id = get_playlist(token, "1y5M6mszA1o2DHbAuHm0av")

# # The Playlist
# playlist_tracks = get_playlist(token, "5SdNXp2VzTmw6KYdvvRrdz")

# # Collast
# playlist_tracks = get_playlist(token, "2dhCDJRi7pufsCBUUynQbQ")

# Mellifrial
playlist_id = get_playlist(access_token, "3vZey3WJogJd0zwEpSTe0V")

# # Alaina's Playlist
# playlist_id = get_playlist(access_token, "2P8yzOS7wPcQhui43927H4")

# # Jingming's Playlist
# playlist_id = get_playlist(access_token, "3PFSJbGSOIkrNWOfrjfvFI")

#print( len(playlist_id))

# Using Random.org's api to get a random value and use that to
# randomly pick a song from a given playlist
if playlist_id:
    random_index = get_random_number(0, len(playlist_id)-1)
    random_song = playlist_id[random_index]
    print(f"The Song for {month} {day_w_suffix}, {year} is: {random_song}")
    print(f"The random index is: {random_index}/{len(playlist_id)}")
else:
    print("List is empty/No song found in playlist")

# # Gets your top tracks (broken, Valid User Authentication Required)
# top_tracks = get_top_tracks(access_token)
# print("Your top 10 tracks within the past week are:")
# for track in top_tracks:
#     print(f"{track['rank']}. {track['name']} by {track[' artists']} (ID: {track['id']})")





# # Using python's random module to randomly pick a song
# if playlist_id:
#     random_song = random.choice(playlist_id)
#     print(f"Randomly chosen song of today is: {random_song}")
# else:
#     print("No songs found in playlist")

# Lists out all of the songs in a playlist from top to bottom in numerical order
# for idx, track in enumerate(playlist_tracks):
#     print(f"{idx + 1}. {track}")


# for idx, song in enumerate(result):
#     print(f"{idx + 1}. {song['name']}")
# result = search_for_artist(token, "sleep token")
# print(result["name"])
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)
# # print(songs)
# for idx, song in enumerate(songs):
#    print(f"{idx + 1}. {song['name']}")
# print(token)

# # Finds any duplicate songs in a playlist, does not factor in length time
# if playlist_id:
#     print("Before running remove_duplicates...")
#     track_counts = Counter(playlist_id)
#     duplicates = {track: count for track, count in track_counts.items() if count > 1}
#     if duplicates:
#         print("Duplicate tracks found:")
#         for track, count in duplicates.items():
#             print(f"{track}: {count} times")
#     else:
#         print("No duplicates found")
# else:
#     print("No songs in playlist")

#
# if playlist_id:
#     print("After running remove_duplicates...")
#     track_counts = Counter(playlist_id)
#     duplicates = {track: count for track, count in track_counts.items() if count > 1}
#     if duplicates:
#         print("Duplicate tracks found:")
#         for track, count in duplicates.items():
#             print(f"{track}: {count} times")
#     else:
#         print("No duplicates found")
# else:
#     print("No songs in playlist")
