import os
import requests
import yt_dlp
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = "AIzaSyAxSg2uRGJ2eZ1nEhr_oEYeawkGXPkBulA"
@app.route("/get_related_music", methods=["GET"])
def get_related_music():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    # Step 1: Fetch Video Details
    video_details_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
    video_response = requests.get(video_details_url)
    video_data = video_response.json()

    if "items" not in video_data or not video_data["items"]:
        return jsonify({"error": "Failed to fetch video details"}), 500

    video_title = video_data["items"][0]["snippet"]["title"]
    video_channel = video_data["items"][0]["snippet"]["channelTitle"]

    # Step 2: Search for Similar Music
    search_query = f"{video_title} {video_channel} music"
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&videoCategoryId=10&maxResults=10&q={search_query}&key={YOUTUBE_API_KEY}"
    
    search_response = requests.get(search_url)
    search_data = search_response.json()

    if "items" not in search_data:
        return jsonify({"error": "Failed to fetch related music"}), 500

    related_music = [
        {
            "videoId": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        }
        for item in search_data["items"]
    ]

    return jsonify({"related_music": related_music})
    

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
def search_music_with_audio():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&videoCategoryId=10&regionCode=IN&maxResults=10&q={query}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "items" not in data:
        return jsonify({"error": "Failed to fetch search results"}), 500

    search_results = []
    for item in data["items"]:
        if "shorts" in item["snippet"]["title"].lower() or "shorts" in item["snippet"]["description"].lower():
            continue
        
        video_id = item["id"]["videoId"]
        video_title = item["snippet"]["title"]
        thumbnail = item["snippet"]["thumbnails"]["high"]["url"]

        
        search_results.append({
            "videoId": video_id,
            "title": video_title,
            "thumbnail": thumbnail,
          
        })

    return jsonify({"search_results": search_results})


@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400
    
    audio_url = get_audio_url(video_id)
    if not audio_url:
        return jsonify({"error": "Failed to get audio URL"}), 500
    
    return jsonify({"videoId": video_id, "audioUrl": audio_url})


@app.route("/download_audio", methods=["GET"])
def download_audio():
    audio_url = request.args.get("audioUrl")
    file_name = request.args.get("fileName", "audio.mp3")
    if not audio_url:
        return jsonify({"error": "Missing 'audioUrl' parameter"}), 400
    
    try:
        response = requests.get(audio_url, stream=True)
        file_path = os.path.join("downloads", file_name)
        os.makedirs("downloads", exist_ok=True)
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/about_us", methods=["GET"])
def about_us():
    return jsonify({
        "name": "Music API",
        "version": "1.0",
        "description": "An API to fetch trending music, search songs, and get audio streams from YouTube.",
        "developer": "Your Name"
    })

def is_short_video(duration):
    if "M" not in duration and "H" not in duration:
        return True  # Video is less than 1 minute (Shorts)
    return False

def get_audio_url(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            return info_dict["url"]
    except Exception as e:
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
