import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
import yt_dlp

# -----------------------------
# CONFIG
# -----------------------------
SPOTIFY_CLIENT_ID = "52df20d52cfc497b8d855d65e36ca804"
SPOTIFY_CLIENT_SECRET = "71e35b53b2b24895a8cc5341da1f9e26"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# -----------------------------
# SPOTIFY AUTH
# -----------------------------
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
))

# -----------------------------
# Get Liked Songs
# -----------------------------
def get_liked_songs():
    results = sp.current_user_saved_tracks()
    songs = []

    while results:
        for item in results['items']:
            track = item['track']
            name = track['name']
            artist = track['artists'][0]['name']
            songs.append(f"{name} {artist}")
        if results['next']:
            results = sp.next(results)
        else:
            break

    return songs
# -----------------------------
# Download using yt-dlp
# -----------------------------
def download_audio(url, title):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/{title}.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# -----------------------------
# Run All
# -----------------------------
if __name__ == "__main__":
    songs = get_liked_songs()
    print(f"Total songs: {len(songs)}")

    for song in songs:
        print(f"\nSearching: {song}")
        url = search_youtube(song)
        print(f"Found: {url}")

        print("Downloading...")
        download_audio(url, song)

    print("\nAll downloads complete!")
input("\nPress Enter to exit...")

