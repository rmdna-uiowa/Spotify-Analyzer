# main.py
import os
import json
from datetime import datetime
from spotify import get_token, get_playlist
from utils import get_random_number, get_ordinal_suffix

playlist_name = "MELLIFRIAL"
playlist_id = os.getenv(playlist_name)
playlist_file = f"{playlist_name}.json"


def save_playlist(playlist, filename=playlist_file):
    """Save the playlist list to a JSON file."""
    with open(filename, "w") as f:
        json.dump(playlist, f, indent=4, ensure_ascii=False)

def load_playlist(filename=playlist_file):
    """Load the playlist list from a JSON file if it exists."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return None

choice = input("Rerun? (Y/N): ").strip().lower()

if choice == 'y':
    # Re-fetch the playlist from Spotify
    access_token = get_token()
    playlist_tracks = get_playlist(access_token, playlist_id)
    if playlist_tracks:
        save_playlist(playlist_tracks)
    else:
        print("Spotify returned an empty list. Trying to load the last saved playlist...")
        playlist_tracks = load_playlist()
else:
    # Load the previously saved playlist, or fetch if not available
    playlist_tracks = load_playlist()
    if playlist_tracks is None:
        print("No saved playlist found. Fetching from Spotify...")
        access_token = get_token()
        playlist_tracks = get_playlist(access_token, playlist_id)
        if playlist_tracks:
            save_playlist(playlist_tracks)

if playlist_tracks:
    # Get current date details
    today = datetime.now()
    month = today.strftime("%B")
    day = today.day
    year = today.year
    day_suffix = get_ordinal_suffix(day)

    # Get a random index from the playlist
    random_index = get_random_number(0, len(playlist_tracks) - 1)
    random_song = playlist_tracks[random_index]
    print(f"The Song for {month} {day}{day_suffix}, {year} is: {random_song}")
    print(f"The random index is: {random_index}/{len(playlist_tracks)}")
else:
    print("List is empty/No song found in playlist")
