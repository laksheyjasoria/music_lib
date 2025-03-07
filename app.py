import os
import requests
import yt_dlp
from datetime import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from collections import defaultdict


app = Flask(__name__)
CORS(app)

# Load YouTube API Key
YT_API_KEY = os.getenv("API_KEY")
if not YT_API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")

song_play_count = defaultdict(lambda: {"count": 0, "title": "", "thumbnail": "","duration":""})

@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400
    return get_audio_method(video_id)

def get_audio_method(video_id):
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

@app.route("/get_details", methods=["GET"])
def get_details():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400
    return jsonify(get_video_details(video_id))

def get_video_details(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {"quiet": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),  # Duration in seconds
        }

    except Exception as e:
        print(f"Error fetching video details: {e}")
        return None

cached_trending_music = []
last_refresh_time = None

@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    global cached_trending_music, last_refresh_time

    # If cache is empty or data is older than 24 hours, refresh it
    if not cached_trending_music or (last_refresh_time and datetime.now() - last_refresh_time > timedelta(days=1)):
        print("this time we fetch the data")
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&chart=mostPopular&videoCategoryId=10&regionCode=IN&maxResults=50&key={YT_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "items" not in data:
            return jsonify({"error": "Failed to fetch trending music"}), 500

        cached_trending_music = [
            {
                "videoId": item["id"],
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }
            for item in data["items"]
        ]
        
        last_refresh_time = datetime.now()  # Update last refresh timestamp

    return jsonify({"trending_music": cached_trending_music})

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

        video_details = get_audio_method(video_id)
        if video_details and video_details["duration"] >= 60:  # ✅ Filter short videos
            search_results.append({
                "videoId": video_id,
                "title": video_details["title"],
                "thumbnail": video_details["thumbnail"],
            })


    return jsonify({"search_results": search_results})

def get_audio_url(video_id):
    try:
        ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info_dict["url"]
    except Exception as e:
        print(f"Error extracting audio URL: {e}")
        return None

@app.route("/about_us", methods=["GET"])
def about_us():
    return jsonify({
        "name": "Noizzify",
        "version": "1.0",
        "description": "An API to fetch trending music, search songs, and get audio streams from YouTube.",
        "developer": "Lakshey Kumar :)"
    })

# Ensure correct port binding for Railway
PORT = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
