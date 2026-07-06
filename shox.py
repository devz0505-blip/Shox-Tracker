import requests
import json
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

ARTIST_ID = "4qemKfpJPX6zS00wWwUQbZ"

CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]

def get_token():
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )

    print(r.status_code)
    print(r.text)

    r.raise_for_status()
    return r.json()["access_token"]

token = get_token()

headers = {
    "Authorization": f"Bearer {token}"
}

r = requests.get(
    f"https://api.spotify.com/v1/artists/{ARTIST_ID}",
    headers=headers
)

print(r.status_code)
print(r.text)
exit()

latest = r.json()["items"][0]

release_id = latest["id"]

try:
    with open("last_release.txt", "r") as f:
        last_id = f.read().strip()
except:
    last_id = ""

if release_id == last_id:
    print("Schon gepostet")
    exit()

name = latest["name"]
url = latest["external_urls"]["spotify"]

requests.post(
    WEBHOOK,
    json={
        "content": f"🎵 Neuer Release von SHOX!\n\n{name}\n{url}"
    }
)

with open("last_release.txt", "w") as f:
    f.write(release_id)
