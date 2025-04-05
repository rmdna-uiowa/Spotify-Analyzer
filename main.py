# main.py
import os
from datetime import datetime
from spotify import get_token, get_playlist
from utils import get_random_number, get_ordinal_suffix

playlist_id = os.getenv('MELLIFRIAL')

# Get current date details
today = datetime.now()
month = today.strftime("%B")
day = today.day
year = today.year
day_suffix = get_ordinal_suffix(day)

# Get Spotify access token
access_token = get_token()

# Replace with your desired playlist ID
playlist_tracks = get_playlist(access_token, playlist_id)

if playlist_tracks:
    random_index = get_random_number(0, len(playlist_tracks) - 1)
    random_song = playlist_tracks[random_index]
    print(f"The Song for {month} {day}{day_suffix}, {year} is: {random_song}")
    print(f"The random index is: {random_index}/{len(playlist_tracks)}")
else:
    print("List is empty/No song found in playlist")
