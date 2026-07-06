import requests
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

ARTIST_ID = "4qemKfpJPX6zS00WwWUQbZ"

CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]


def get_token():
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )

    r.raise_for_status()
    return r.json()["access_token"]


token = get_token()

headers = {
    "Authorization": f"Bearer {token}"
}

r = requests.get(
    f"https://api.spotify.com/v1/artists/{ARTIST_ID}/albums",
    headers=headers,
    params={
        "include_groups": "single,album",
        "market": "DE",
        "limit": 1
    }
)

r.raise_for_status()

data = r.json()

if not data.get("items"):
    print("Keine Releases gefunden.")
    exit()

latest = data["items"][0]

release_id = latest["id"]
name = latest["name"]
url = latest["external_urls"]["spotify"]
cover = latest["images"][0]["url"]
release_date = latest["release_date"]
album_type = latest["album_type"].capitalize()

try:
    with open("last_release.txt", "r") as f:
        last_id = f.read().strip()
except FileNotFoundError:
    last_id = ""

if release_id == last_id:
    print("Schon gepostet.")
    exit()

embed = {
    "title": "🔥 Neue Release von SHOX!",
    "description": f"## 🎵 {name}\nNeue Single von **SHOX** ist jetzt auf Spotify verfügbar.",
    "url": url,
    "color": 0x8A2BE2,

   "author": {
    "name": "SHOX",
    "icon_url": "https://cdn.discordapp.com/attachments/734182009618038856/1523689983448318232/WhatsApp_Image_2026-05-11_at_01.38.04.jpeg?ex=6a4d0660&is=6a4bb4e0&hm=900c3e78021df6f8995e8f731062ae6c2b277daf65e5b484d23d92684506257a&"
},

    "thumbnail": {
        "url": cover
    },

    "image": {
        "url": cover
    },

    "fields": [
        {
            "name": "📅 Veröffentlichungsdatum",
            "value": release_date,
            "inline": True
        },
        {
            "name": "💿 Typ",
            "value": album_type,
            "inline": True
        },
        {
            "name": "🎧 Spotify",
            "value": f"[Jetzt anhören]({url})",
            "inline": False
        }
    ],

    "footer": {
        "text": "SHOX Release Tracker"
    }
}

requests.post(
    WEBHOOK,
    json={
        "username": "SHOX Tracker",
        "embeds": [embed]
    }
)

with open("last_release.txt", "w") as f:
    f.write(release_id)

print("Neue Release gepostet!")
