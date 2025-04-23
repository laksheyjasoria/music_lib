# import os
# import requests
# import yt_dlp
# import datetime
# from flask import Flask, jsonify, request, send_file
# from flask_cors import CORS
# from collections import defaultdict
# from pydub import AudioSegment
# from io import BytesIO
# import re
# import audio
# import audioV2
# import utils
# from itertools import chain

# app = Flask(__name__)
# CORS(app)

# # Load YouTube API Key
# YT_API_KEY = os.getenv("API_KEY")
# if not YT_API_KEY:
#     raise ValueError("API_KEY is not set in environment variables.")

# song_play_count = defaultdict(lambda: {"count": 0, "title": "", "thumbnail": ""})

# # Global list to store unique search results
# unique_search_results = []


# # Cache for trending music
# cached_trending_music = []
# last_trending_fetch = None  # Track last fetch time


# @app.route("/get_audio", methods=["GET"])
# def get_audio():
#     video_id = request.args.get("videoId")
#     if not video_id:
#         return jsonify({"error": "Missing 'videoId' parameter"}), 400

#     # Find the video details in the search_results list
#     # video_details = next((video for video in unique_search_results if video["videoId"] == video_id), None)
#     video_details = next((video for video in chain(unique_search_results, cached_trending_music) if video.get("videoId") == video_id),None)

#     if video_details:
#         song_play_count[video_id].update({
#             "title": video_details["title"],
#             "thumbnail": video_details["thumbnail"]
#         })
    
#     song_play_count[video_id]["count"] += 1
#     # audio_url = audio.get_audio_url(video_id)
#     audio_url = audioV2.get_audio_url(video_id)
    

#     if not audio_url:
#         return jsonify({"error": "Failed to get audio URL"}), 500

#     return jsonify(
#         {
#             "videoId": video_id,
#             "title": song_play_count[video_id]["title"],
#             "thumbnail": song_play_count[video_id]["thumbnail"],
#             "audioUrl": audio_url,
#         }
#     )


# @app.route("/search_music", methods=["GET"])
# def search_music():
#     """Searches for YouTube music videos and returns results with duration > 60s."""
#     query = request.args.get("query")
#     if not query:
#         return jsonify({"error": "Missing 'query' parameter"}), 400

#     # Step 1: Search for videos
#     search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&videoCategoryId=10&regionCode=IN&maxResults=50&q={query}&key={YT_API_KEY}"
#     search_response = requests.get(search_url).json()

#     if "items" not in search_response:
#         return jsonify({"error": "Failed to fetch search results"}), 500

#     # Extract video IDs
#     video_ids = [item["id"]["videoId"] for item in search_response.get("items", []) if "videoId" in item["id"]]

#     if not video_ids:
#         return jsonify({"search_results": []})  # Return empty if no videos found

#     # Step 2: Fetch video durations
#     details_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={','.join(video_ids)}&key={YT_API_KEY}"
#     details_response = requests.get(details_url).json()

#     search_results = []
#     for item in details_response.get("items", []):
#         video_id = item["id"]
#         video_title = item["snippet"]["title"]
#         thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
#         duration = utils.iso8601_to_seconds(item["contentDetails"]["duration"])

#         if duration >= 90 and video_id not in [res["videoId"] for res in unique_search_results]:  # Only include unique entries
#             result = {
#                 "videoId": video_id,
#                 "title": video_title,
#                 "thumbnail": thumbnail,
#                 "duration": duration
#             }
#             search_results.append(result)
#             unique_search_results.append(result)  # Add to global unique list

#     return jsonify({"search_results": search_results})

# @app.route("/get_trending_music", methods=["GET"])
# def get_trending_music():
#     """Fetches trending music once per day and caches the results."""
#     global cached_trending_music, last_trending_fetch

#     # Check if the cache is expired (older than 24 hours)
#     if not last_trending_fetch or (datetime.datetime.now() - last_trending_fetch).days >= 1:
#         url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&chart=mostPopular&videoCategoryId=10&regionCode=IN&maxResults=30&key={YT_API_KEY}"
#         response = requests.get(url)
#         data = response.json()

#         if "items" not in data:
#             return jsonify({"error": "Failed to fetch trending music"}), 500

#         # Update cache
#         cached_trending_music = [
#             {
#                 "videoId": item["id"],
#                 "title": item["snippet"]["title"],
#                 "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
#             }
#             for item in data["items"]
#         ]
#         last_trending_fetch = datetime.datetime.now()

#     return jsonify({"trending_music": cached_trending_music})

# @app.route("/get_most_played_songs", methods=["GET"])
# def get_most_played_songs():
#     sorted_songs = sorted(song_play_count.items(), key=lambda x: x[1]["count"], reverse=True)
#     most_played_songs = [
#         {
#             "videoId": video_id,
#             "title": data["title"],
#             "thumbnail": data["thumbnail"],
#             "play_count": data["count"],
#         }
#         for video_id, data in sorted_songs[:50]
#     ]
#     return jsonify({"most_played_songs": most_played_songs})

# # Ensure correct port binding for Railway
# PORT = int(os.getenv("PORT", 5000))

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=PORT, debug=True)

# app.py (updated)
from flask import Flask, jsonify, request
from flask_cors import CORS
from services import YouTubeService
from audio_service import AudioService
from song import Song
import os
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# Initialize services
yt_service = YouTubeService(os.getenv("API_KEY"))
audio_service = AudioService()
playback_stats = defaultdict(Song)

@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing videoId"}), 400

    song = playback_stats.get(video_id)
    if not song:
        song = yt_service.get_video_details(video_id)
        if not song:
            return jsonify({"error": "Invalid videoId"}), 404
        playback_stats[video_id] = song

    song.increment_play_count()
    audio_url = audio_service.get_audio_url(video_id)
    
    return jsonify({
        **song.to_dict(),
        "audioUrl": audio_url
    }) if audio_url else jsonify({"error": "Failed to get audio"}), 500

@app.route("/trending", methods=["GET"])
def get_trending():
    try:
        trending = yt_service.get_trending()
        return jsonify([song.to_dict() for song in trending])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/most_played", methods=["GET"])
def get_most_played():
    sorted_songs = sorted(playback_stats.values(), 
                        key=lambda s: s.play_count, 
                        reverse=True)[:50]
    return jsonify([song.to_dict() for song in sorted_songs])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
