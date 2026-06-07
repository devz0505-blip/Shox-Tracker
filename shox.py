import requests
import json
import os

WEBHOOK = "https://discord.com/api/webhooks/1511520888963465376/WHvr_TSWrabk0H8X4k4J0INg6T1JIulx--DvM3ZA2Gls1Gg5IgHK6SgcCVgW1aHYqw0m"

ARTIST_ID = "4qemKfJpXP6zS0OWvWUQbZ"

CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]

def get_token():
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    return r.json()["access_token"]

token = get_token()

headers = {
    "Authorization": f"Bearer {token}"
}

r = requests.get(
    f"https://api.spotify.com/v1/artists/{ARTIST_ID}/albums?include_groups=single,album",
    headers=headers
)

latest = r.json()["items"][0]

name = latest["name"]
url = latest["external_urls"]["spotify"]

requests.post(
    WEBHOOK,
    json={
        "content": f"🎵 Neuer Release von SHOX!\n\n{name}\n{url}"
    }
)
