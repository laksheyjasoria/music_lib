import os
import requests
import yt_dlp
from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = "AIzaSyAxSg2uRGJ2eZ1nEhr_oEYeawkGXPkBulA"
music_queue = []


@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&chart=mostPopular&videoCategoryId=10&regionCode=IN&maxResults=20&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data:
        return jsonify({"error": "Failed to fetch trending music"}), 500

    trending_music = [
        {
            "videoId": item["id"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "duration": item["contentDetails"]["duration"]
        }
        for item in data["items"]
        if "shorts" not in item["snippet"]["title"].lower() and "shorts" not in item["snippet"]["description"].lower() and not is_short_video(item["contentDetails"]["duration"])
    ]

    return jsonify({"trending_music": trending_music})



@app.route("/search_music", methods=["GET"])
def search_music():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&videoCategoryId=10&regionCode=IN&maxResults=20&q={query}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data:
        return jsonify({"error": "Failed to fetch search results"}), 500

    search_results = [
        {
            "videoId": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        }
        for item in data["items"]
        if "shorts" not in item["snippet"]["title"].lower() and "shorts" not in item["snippet"]["description"].lower()
    ]

    return jsonify({"search_results": search_results})


@app.route("/get_suggested_music", methods=["GET"])
def get_suggested_music():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&relatedToVideoId={video_id}&type=video&videoCategoryId=10&regionCode=IN&maxResults=10&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data:
        return jsonify({"error": "Failed to fetch suggestions"}), 500

    suggested_music = [
        {
            "videoId": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        }
        for item in data["items"]
        if "shorts" not in item["snippet"]["title"].lower() and "shorts" not in item["snippet"]["description"].lower()
    ]

    return jsonify({"suggested_music": suggested_music})


@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            audio_url = info_dict["url"]
        
        return jsonify({"videoId": video_id, "audioUrl": audio_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/add_to_queue", methods=["POST"])
def add_to_queue():
    data = request.json
    if "videoId" not in data or "title" not in data:
        return jsonify({"error": "Missing 'videoId' or 'title'"}), 400

    music_queue.append(data)
    return jsonify({"message": "Added to queue", "queue": music_queue})


@app.route("/shuffle_queue", methods=["GET"])
def shuffle_queue():
    random.shuffle(music_queue)
    return jsonify({"message": "Queue shuffled", "queue": music_queue})


@app.route("/skip", methods=["GET"])
def skip_song():
    if music_queue:
        music_queue.pop(0)
    return jsonify({"message": "Skipped", "queue": music_queue})


@app.route("/repeat", methods=["GET"])
def repeat_song():
    if music_queue:
        music_queue.append(music_queue[0])
    return jsonify({"message": "Repeated", "queue": music_queue})


def is_short_video(duration):
    if "M" not in duration and "H" not in duration:
        return True  # Video is less than 1 minute (Shorts)
    return False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
