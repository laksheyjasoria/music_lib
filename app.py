import os
import requests
import yt_dlp
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# Load YouTube API Key
YT_API_KEY = os.getenv("API_KEY")
if not YT_API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")

song_play_count = defaultdict(lambda: {"count": 0, "title": "", "thumbnail": ""})

@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    if song_play_count.get(video_id, {}).get("count", 0) == 0:
        video_details = get_video_details(video_id)
        if not video_details:
            return jsonify({"error": "Failed to fetch video details"}), 500
        song_play_count[video_id]["title"] = video_details["title"]
        song_play_count[video_id]["thumbnail"] = video_details["thumbnail"]

    song_play_count[video_id]["count"] += 1
    audio_url = get_audio_url(video_id)

    if not audio_url:
        return jsonify({"error": "Failed to get audio URL"}), 500

    return jsonify({
        "videoId": video_id,
        "title": song_play_count[video_id]["title"],
        "thumbnail": song_play_count[video_id]["thumbnail"],
        "audioUrl": audio_url
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
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YT_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data or not data["items"]:
        return None

    video_info = data["items"][0]["snippet"]
    return {
        "title": video_info["title"],
        "thumbnail": video_info["thumbnails"]["high"]["url"]
    }

@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
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

        search_results.append({
            "videoId": video_id,
            "title": video_title,
            "thumbnail": thumbnail,
        })

    return jsonify({"search_results": search_results})

@app.route("/download_audio", methods=["GET"])
def download_audio():
    video_id = request.args.get("videoId")

    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    try:
        video_details = get_video_details(video_id)
        if not video_details:
            return jsonify({"error": "Failed to retrieve video details"}), 500

        title = video_details["title"]
        sanitized_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
        file_name = f"{sanitized_title}.mp3"

        audio_url = get_audio_url(video_id)
        if not audio_url:
            return jsonify({"error": "Failed to retrieve audio URL"}), 500

        response = requests.get(audio_url, stream=True)
        response.raise_for_status()

        file_path = os.path.join("downloads", file_name)
        os.makedirs("downloads", exist_ok=True)

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        return send_file(file_path, as_attachment=True)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to download: {str(e)}"}), 500

def get_audio_url(video_id):
    try:
        ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info_dict["url"]
    except Exception as e:
        print(f"Error extracting audio URL: {e}")
        return None

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
