import os
import requests
import yt_dlp
from flask import Flask, jsonify, request
from flask_cors import CORS
from collections import defaultdict
from datetime import date
import re
import ffmpeg
from io import BytesIO

app = Flask(__name__)
CORS(app)


def get_audio_duration(url: str) -> float:
    try:
        # Stream the audio file from the URL
        response = requests.get(url, stream=True)
 
        if response.status_code == 200:
            # Use FFmpeg to probe the metadata from the audio stream
            probe = ffmpeg.probe(url, v='error', select_streams='a', show_entries='stream=duration')
            
            # Extract the duration from the probe result
            duration = float(probe['streams'][0]['duration'])
            return duration
        else:
            print("Error fetching the audio file.")
            return None
 
    except Exception as e:
        print(f"Error: {e}")
        return None

# Load YouTube API Key
YT_API_KEY = os.getenv("API_KEY")
if not YT_API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")

# Dictionary to store song play counts
song_play_count = defaultdict(lambda: {"count": 0, "title": "", "thumbnail": "", "duration": ""})

# Cache for trending music
trending_music_cache = {
    "data": None,
    "last_fetched": None
}

@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    return get_music_details(video_id)

def get_video_duration(video_id):
    """Fetch video duration using yt-dlp without an API key"""
    try:
        ydl_opts = {
            "quiet": True, 
            "noplaylist": True, 
            "skip_download": True  # Avoid downloading the video
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        
        return info.get("duration", 0)  # Duration in seconds
    except Exception as e:
        print(f"Error fetching video duration: {e}")
        return None


@app.route("/get_most_played_songs", methods=["GET"])
def get_most_played_songs():
    sorted_songs = sorted(song_play_count.items(), key=lambda x: x[1]["count"], reverse=True)
    most_played_songs = [
        {
            "videoId": video_id,
            "title": data["title"],
            "thumbnail": data["thumbnail"],
            "play_count": data["count"]
        }
        for video_id, data in sorted_songs[:50]
    ]
    return jsonify({"most_played_songs": most_played_songs})

@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    today = date.today()

    # If data exists and was fetched today, return cached data
    if trending_music_cache["data"] and trending_music_cache["last_fetched"] == today:
        print("Fetching cached trending music data")
        return jsonify({"trending_music": trending_music_cache["data"]})

    # Otherwise, fetch fresh data from YouTube API
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&chart=mostPopular&videoCategoryId=10&regionCode=IN&maxResults=30&key={YT_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data:
        return jsonify({"error": "Failed to fetch trending music"}), 500

    trending_music = []
    for item in data["items"]:
        video_id = item["id"]
        title = item["snippet"]["title"]
        thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
        duration = item["contentDetails"]["duration"]

        # Convert duration to seconds and filter out short videos
        duration_seconds = parse_duration(duration)
        if duration_seconds < 60:
            continue  # Skip videos shorter than 60 seconds

        trending_music.append({
            "videoId": video_id,
            "title": title,
            "thumbnail": thumbnail,
            "duration": duration_seconds
        })

    # Cache the response
    trending_music_cache["data"] = trending_music
    trending_music_cache["last_fetched"] = today
    print("Fetching new trending music data")
    return jsonify({"trending_music": trending_music})

def get_music_details(video_id):
    if song_play_count.get(video_id, {}).get("count", 0) == 0:
        video_details = get_video_details(video_id)
        if not video_details:
            return jsonify({"error": "Failed to fetch video details"}), 500
        song_play_count[video_id]["title"] = video_details["title"]
        song_play_count[video_id]["thumbnail"] = video_details["thumbnail"]
        song_play_count[video_id]["duration"] = video_details["duration"]

    song_play_count[video_id]["count"] += 1
    audio_url = get_audio_url(video_id)

    if not audio_url:
        return jsonify({"error": "Failed to get audio URL"}), 500

    return jsonify({
        "videoId": video_id,
        "title": song_play_count[video_id]["title"],
        "thumbnail": song_play_count[video_id]["thumbnail"],
        "audioUrl": audio_url,
        "duration": song_play_count[video_id]["duration"]
    })

@app.route("/search_music", methods=["GET"])
def search_music():
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
        title = item["snippet"]["title"]
        thumbnail = item["snippet"]["thumbnails"]["high"]["url"]

        # Fetch video details (to get duration)
        duration = get_audio_duration(get_audio_url(video_id))
        if not duration:
            continue

        # Convert duration to seconds and reject short videos
        duration_seconds = duration
        print("asdn :"+duration_seconds)
        if duration_seconds < 60:
            continue  # Skip videos shorter than 60 seconds

        search_results.append({
            "videoId": video_id,
            "title": title,
            "thumbnail": thumbnail,
            "duration": duration_seconds
        })

    return jsonify({"search_results": search_results})

def get_video_details(video_id):
    """Fetch video details including duration using yt-dlp"""
    try:
        ydl_opts = {"quiet": True, "noplaylist": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        
        return {
            "title": info.get("title", "Unknown"),
            "thumbnail": info.get("thumbnail", ""),
            "duration": info.get("duration", 0)  # Duration in seconds
        }
    except Exception as e:
        print(f"Error fetching video details: {e}")
        return None

def parse_duration(duration):
    """Convert ISO 8601 duration format (PT#H#M#S) to total seconds"""
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return 0

    hours = int(match.group(1)) * 3600 if match.group(1) else 0
    minutes = int(match.group(2)) * 60 if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    return hours + minutes + seconds

@app.route("/", methods=["GET"])
def about_us():
    return jsonify({
        "name": "Noizzify",
        "version": "1.0",
        "description": "An API to fetch trending music, search songs, and get audio streams from YouTube.",
        "backenddev": "Lakshey Kumar :)",
        "frontenddev": "Bharat Kumar :)"
    })

def get_audio_url(video_id):
    try:
        ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info_dict["url"]
    except Exception as e:
        print(f"Error extracting audio URL: {e}")
        return None

# Ensure correct port binding for Railway
PORT = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
