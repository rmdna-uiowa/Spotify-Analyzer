# utils.py
import requests
import os

def get_random_number(min_value: int, max_value: int) -> int:
    """
    Fetches a random number from Random.org API.
    """
    api_key = os.getenv('RANDOM_KEY')
    url = "https://api.random.org/json-rpc/4/invoke"
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
    response = requests.post(url, json=payload)
    data = response.json()
    return data["result"]["random"]["data"][0]

def get_ordinal_suffix(day: int) -> str:
    """
    Returns the ordinal suffix for a given day.
    """
    if 10 <= day % 100 <= 20:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
