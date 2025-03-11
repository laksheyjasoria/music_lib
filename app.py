import os
import requests
import yt_dlp
import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from collections import defaultdict
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Load YouTube API Key
YT_API_KEY = os.getenv("API_KEY")
if not YT_API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")

song_play_count = defaultdict(lambda: {"count": 0, "title": "", "thumbnail": ""})

# Cache for trending music
cached_trending_music = []
last_trending_fetch = None  # Track last fetch time

def get_audio_duration(url):
    """Downloads the audio file and returns its duration in seconds."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise error if download fails
        
        audio = AudioSegment.from_file(BytesIO(response.content))
        return len(audio) / 1000  # Convert milliseconds to seconds

    except Exception as e:
        print("Error fetching duration:", e)
        return None

@app.route("/search_music", methods=["GET"])
def search_music():
    """Searches for YouTube music videos and returns results with duration > 60s."""
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&videoCategoryId=10&regionCode=IN&maxResults=50&q={query}&key={YT_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data:
        return jsonify({"error": "Failed to fetch search results"}), 500

    search_results = []
    for item in data["items"]:
        video_id = item["id"]["videoId"]
        video_title = item["snippet"]["title"]
        thumbnail = item["snippet"]["thumbnails"]["high"]["url"]

        # Fetch the audio URL and check duration
        audio_url = get_audio_url(video_id)
        if audio_url:
            duration = get_audio_duration(audio_url)
            if duration and duration > 60:  # Only include if duration > 60 seconds
                search_results.append({
                    "videoId": video_id,
                    "title": video_title,
                    "thumbnail": thumbnail,
                    "duration": duration
                })

    return jsonify({"search_results": search_results})

@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    """Fetches trending music once per day and caches the results."""
    global cached_trending_music, last_trending_fetch

    # Check if the cache is expired (older than 24 hours)
    if not last_trending_fetch or (datetime.datetime.now() - last_trending_fetch).days >= 1:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&chart=mostPopular&videoCategoryId=10&regionCode=IN&maxResults=30&key={YT_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "items" not in data:
            return jsonify({"error": "Failed to fetch trending music"}), 500

        # Update cache
        cached_trending_music = [
            {
                "videoId": item["id"],
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }
            for item in data["items"]
        ]
        last_trending_fetch = datetime.datetime.now()

    return jsonify({"trending_music": cached_trending_music})

def get_audio_url(video_id):
    """Fetches the best audio URL for a given YouTube video ID."""
    try:
        ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info_dict["url"]
    except Exception as e:
        print(f"Error extracting audio URL: {e}")
        return None
@app.route("/get_most_played_songs", methods=["GET"])
def get_most_played_songs():
    sorted_songs = sorted(song_play_count.items(), key=lambda x: x[1]["count"], reverse=True)
    most_played_songs = [
        {
            "videoId": video_id,
            "title": data["title"],
            "thumbnail": data["thumbnail"],
            "play_count": data["count"],
        }
        for video_id, data in sorted_songs[:50]
    ]
    return jsonify({"most_played_songs": most_played_songs})


# Ensure correct port binding for Railway
PORT = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
