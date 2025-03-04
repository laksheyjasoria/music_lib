import os
import yt_dlp
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from collections import defaultdict

app = Flask(__name__)
CORS(app)

song_play_count = defaultdict(lambda: {"count": 0, "title": "", "thumbnail": ""})

@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

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
        "title": video_details["title"],
        "thumbnail": video_details["thumbnail"],
        "audioUrl": audio_url
    })

@app.route("/get_most_played_songs", methods=["GET"])
def get_most_played_songs():
    sorted_songs = sorted(song_play_count.items(), key=lambda x: x[1]["count"], reverse=True)
    most_played_songs = [
        {"videoId": vid, "title": data["title"], "thumbnail": data["thumbnail"], "play_count": data["count"]}
        for vid, data in sorted_songs[:50]
    ]
    return jsonify({"most_played_songs": most_played_songs})

@app.route("/search_music", methods=["GET"])
def search_music():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    search_results = yt_search(query)
    return jsonify({"search_results": search_results})

@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    trending_music = yt_trending()
    return jsonify({"trending_music": trending_music})

@app.route("/download_audio", methods=["GET"])
def download_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    video_details = get_video_details(video_id)
    if not video_details:
        return jsonify({"error": "Failed to retrieve video details"}), 500

    file_name = f"downloads/{video_details['title'].replace(' ', '_')}.mp3"
    os.makedirs("downloads", exist_ok=True)

    try:
        ydl_opts = {"format": "bestaudio/best", "outtmpl": file_name}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        return send_file(file_name, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Failed to download: {str(e)}"}), 500

# Helper functions
def get_video_details(video_id):
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return {"title": info["title"], "thumbnail": info["thumbnail"]}
    except Exception as e:
        print(f"Error fetching video details: {e}")
        return None

def get_audio_url(video_id):
    try:
        with yt_dlp.YoutubeDL({"format": "bestaudio/best", "quiet": True}) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info_dict["url"]
    except Exception as e:
        print(f"Error extracting audio URL: {e}")
        return None

def yt_search(query):
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            result = ydl.extract_info(f"ytsearch50:{query}", download=False)
            return [{"videoId": vid["id"], "title": vid["title"], "thumbnail": vid["thumbnail"]} for vid in result["entries"]]
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []

def yt_trending():
    return yt_search("Trending Music")

@app.route("/about_us", methods=["GET"])
def about_us():
    return jsonify({
        "name": "Noizzify",
        "version": "2.0",
        "description": "An API to fetch trending music, search songs, and get audio streams from YouTube using yt-dlp.",
        "developer": "Lakshey Kumar :)"
    })

if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
