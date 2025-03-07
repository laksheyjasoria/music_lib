import os
import requests
import yt_dlp
from flask import Flask, jsonify, request
from flask_cors import CORS
from collections import defaultdict
from datetime import date

app = Flask(__name__)
CORS(app)

# Load YouTube API Key
YT_API_KEY = os.getenv("API_KEY")
if not YT_API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")

song_play_count = defaultdict(lambda: {"count": 0, "title": "", "thumbnail": "", "duration": ""})

@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    return get_music_details(video_id)

def get_music_details(video_id):
    if song_play_count.get(video_id, {"count": 0}).get("count", 0) == 0:
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

# Trending Music Caching
trending_music_cache = {
    "data": None,
    "last_fetched": None
}

@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    today = date.today()

    if trending_music_cache["data"] and trending_music_cache["last_fetched"] == today:
        return jsonify({"trending_music": trending_music_cache["data"]})

    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&chart=mostPopular&videoCategoryId=10&regionCode=IN&maxResults=30&key={YT_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data:
        return jsonify({"error": "Failed to fetch trending music"}), 500

    trending_music = [
        {
            "videoId": item["id"],
            "title": item["snippet"]["title"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        }
        for item in data["items"]
    ]

    trending_music_cache["data"] = trending_music
    trending_music_cache["last_fetched"] = today

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
        video_title = item["snippet"]["title"]
        thumbnail = item["snippet"]["thumbnails"]["high"]["url"]

        video_details = get_video_details(video_id)
        if not video_details:
            continue

        duration_seconds = parse_duration(video_details["duration"])
        if duration_seconds < 60:
            continue

        search_results.append({
            "videoId": video_id,
            "title": video_title,
            "thumbnail": thumbnail,
            "duration": video_details["duration"]
        })

    return jsonify({"search_results": search_results})

def parse_duration(duration):
    import re
    match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
    hours = int(match.group(1)[:-1]) * 3600 if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) * 60 if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
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

PORT = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
