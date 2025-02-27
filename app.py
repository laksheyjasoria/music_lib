import os
import yt_dlp
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return "YouTube Audio Extractor API is Running!"

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
            "quiet": True,
            "extract_flat": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            audio_url = info_dict["url"]
        
        return jsonify({"videoId": video_id, "audioUrl": audio_url})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

YOUTUBE_API_KEY = "AIzaSyAxSg2uRGJ2eZ1nEhr_oEYeawkGXPkBulA"  # Replace with your API key

@app.route("/get_suggestions", methods=["GET"])
def get_suggestions():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    # YouTube API URL for related videos
    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&relatedToVideoId={video_id}&type=video&key={YOUTUBE_API_KEY}&maxResults=30"

    try:
    response = requests.get(youtube_url)
    data = response.json()

    if "items" not in data:
        return jsonify({"error": "Failed to fetch suggestions"}), 500

    suggestions = []
    for item in data["items"]:
        suggestions.append({
            "videoId": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        })

    return jsonify({"videoId": video_id, "suggestions": suggestions})

except Exception as e:  # <-- Add this except block
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
