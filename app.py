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

# Dictionary to track song play count
song_play_count = defaultdict(lambda: {"count": 0, "title": "", "thumbnail": ""})

# ------------------ 1️⃣ GET TRENDING MUSIC (INDIA REGION) ------------------
@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    try:
        ydl_opts = {
            "quiet": True,
            "default_search": "ytsearch20",
            "noplaylist": True,
            "extract_flat": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            trending_results = ydl.extract_info("Trending music India", download=False)

        trending_songs = []
        for entry in trending_results.get("entries", []):
            video_id = entry.get("id")
            video_details = get_video_details(video_id)

            if video_details and video_details["duration"] > 60:  # Exclude Shorts
                trending_songs.append(video_details)

        return jsonify({"trending_music": trending_songs})

    except Exception as e:
        return jsonify({"error": f"Error fetching trending music: {e}"}), 500


# ------------------ 2️⃣ SEARCH MUSIC ------------------
@app.route("/search_music", methods=["GET"])
def search_music():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    ydl_opts = {"quiet": True, "default_search": "ytsearch50", "noplaylist": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(query, download=False)

        search_songs = [
            {
                "videoId": item["id"],
                "title": item["title"],
                "thumbnail": item["thumbnail"],
                "duration": item["duration"],
            }
            for item in search_results["entries"]
            if item["duration"] > 60  # Exclude Shorts
        ]
        return jsonify({"search_results": search_songs})

    except Exception as e:
        return jsonify({"error": f"Failed to fetch search results: {e}"}), 500


# ------------------ 3️⃣ GET AUDIO STREAM URL ------------------
@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    if song_play_count[video_id]["count"] == 0:
        video_details = get_video_details(video_id)
        if video_details:
            song_play_count[video_id].update(video_details)

    song_play_count[video_id]["count"] += 1
    audio_url = get_audio_url(video_id)

    if not audio_url:
        return jsonify({"error": "Failed to get audio URL"}), 500

    return jsonify(
        {
            "videoId": video_id,
            "title": song_play_count[video_id]["title"],
            "thumbnail": song_play_count[video_id]["thumbnail"],
            "audioUrl": audio_url,
        }
    )


# ------------------ 4️⃣ DOWNLOAD AUDIO ------------------
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


# ------------------ 5️⃣ GET MOST PLAYED SONGS ------------------
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


# ------------------ 6️⃣ MANAGE PLAYLISTS ------------------
playlists = {}

@app.route("/create_playlist", methods=["POST"])
def create_playlist():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing playlist name"}), 400
    playlists[name] = []
    return jsonify({"message": f"Playlist '{name}' created successfully"})


@app.route("/add_to_playlist", methods=["POST"])
def add_to_playlist():
    data = request.json
    playlist_name = data.get("playlist")
    video_id = data.get("videoId")

    if playlist_name not in playlists:
        return jsonify({"error": "Playlist not found"}), 404

    video_details = get_video_details(video_id)
    if not video_details:
        return jsonify({"error": "Invalid video ID"}), 400

    playlists[playlist_name].append(video_details)
    return jsonify({"message": f"Song added to '{playlist_name}'"})


@app.route("/get_playlist", methods=["GET"])
def get_playlist():
    name = request.args.get("name")
    if not name or name not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    return jsonify({"playlist": playlists[name]})


# ------------------ HELPER FUNCTIONS ------------------
def get_video_details(video_id):
    try:
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return {
                "videoId": video_id,
                "title": info.get("title"),
                "thumbnail": info["thumbnail"],
                "duration": info["duration"],
            }
    except Exception as e:
        return None


def get_audio_url(video_id):
    try:
        ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info_dict["url"]
    except Exception:
        return None


# ------------------ RUN THE APP ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
