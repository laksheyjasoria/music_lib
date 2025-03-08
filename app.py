import os
import requests
import yt_dlp
from flask import Flask, jsonify, request
from flask_cors import CORS
from collections import defaultdict
from datetime import date
import re

app = Flask(__name__)
CORS(app)

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


@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    today = date.today()

    # If data exists and was fetched today, return cached data
    if trending_music_cache["data"] and trending_music_cache["last_fetched"] == today:
        print("this we are fetching previously found data")
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
    print("this we are fetching new found data")
    return jsonify({"trending_music": trending_music})


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
        video_details = get_video_details(video_id)
        if not video_details:
            continue

        # Convert duration to seconds and reject short videos
        duration_seconds = parse_duration(video_details["duration"])
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
    """Fetch video details including duration"""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,snippet&id={video_id}&key={YT_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data or not data["items"]:
        return None

    item = data["items"][0]
    return {
        "title": item["snippet"]["title"],
        "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
        "duration": item["contentDetails"]["duration"]
    }


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


# Ensure correct port binding for Railway
PORT = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
