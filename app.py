import os
import requests
import yt_dlp
import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from collections import defaultdict
from pydub import AudioSegment
from io import BytesIO
import re
import audio
import audioV2
import utils
import cookies_Extractor
import song_extractor
from itertools import chain

app = Flask(__name__)
CORS(app)

# Load YouTube API Key
YT_API_KEY = os.getenv("API_KEY")
if not YT_API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")

song_play_count = defaultdict(lambda: {"count": 0, "title": "", "thumbnail": ""})

# Global list to store unique search results
unique_search_results = []


# Cache for trending music
cached_trending_music = []
last_trending_fetch = None  # Track last fetch time


@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    # Find the video details in the search_results list
    # video_details = next((video for video in unique_search_results if video["videoId"] == video_id), None)
    video_details = next((video for video in chain(unique_search_results, cached_trending_music) if video.get("videoId") == video_id),None)

    if video_details:
        song_play_count[video_id].update({
            "title": video_details["title"],
            "thumbnail": video_details["thumbnail"]
        })
    
    song_play_count[video_id]["count"] += 1
    # audio_url = audio.get_audio_url(video_id)
    audio_url = audioV2.get_audio_url(video_id)
    

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

#         if duration >= 90 and duration<=1200 and video_id not in [res["videoId"] for res in unique_search_results]:  # Only include unique entries
#             result = {
#                 "videoId": video_id,
#                 "title": video_title,
#                 "thumbnail": thumbnail,
#                 "duration": duration
#             }
#             search_results.append(result)
#             unique_search_results.append(result)  # Add to global unique list

#     return jsonify({"search_results": search_results})

@app.route("/search_music", methods=["GET"])
def search_music():
    """Search YouTube music videos with enhanced filters and sorting"""
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    # Step 1: Search for videos
    search_url = (
        f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video"
        f"&videoCategoryId=10&regionCode=IN&maxResults=50&q={query}&key={YT_API_KEY}"
    )
    search_response = requests.get(search_url).json()

    if "items" not in search_response:
        return jsonify({"error": "Failed to fetch search results"}), 500

    # Extract video IDs
    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])
                 if "videoId" in item.get("id", {})]

    if not video_ids:
        return jsonify({"search_results": []})

    # Step 2: Fetch detailed video information
    details_url = (
        f"https://www.googleapis.com/youtube/v3/videos?"
        f"part=snippet,contentDetails,statistics&id={','.join(video_ids)}&key={YT_API_KEY}"
    )
    details_response = requests.get(details_url).json()

    # Filter criteria
    excluded_keywords = {"lofi", "slowed", "reverb", "nightcore", "chill mix", "study beats"}
    min_duration = 90
    max_duration = 1200

    filtered_results = []
    for item in details_response.get("items", []):
        try:
            video_id = item["id"]
            video_title = item["snippet"]["title"]
            title_lower = video_title.lower()
            duration = utils.iso8601_to_seconds(item["contentDetails"]["duration"])
            likes = int(item["statistics"].get("likeCount", 0))

            if (
                any(kw in title_lower for kw in excluded_keywords)
                or not (min_duration <= duration <= max_duration)
                or any(res["videoId"] == video_id for res in unique_search_results)
            ):
                continue

            filtered_results.append({
                "videoId": video_id,
                "title": video_title,
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "duration": duration,
                "likes": likes
            })

        except KeyError as e:
            app.logger.error(f"Missing key in YouTube response: {str(e)}")
            continue
        except Exception as e:
            app.logger.error(f"Error while processing video data: {str(e)}")
            continue

    # Sort by likes descending, then duration ascending
    sorted_results = sorted(
        filtered_results,
        key=lambda x: (-x["likes"], x["duration"])
    )

    # Prevent duplicate entries
    existing_ids = {r["videoId"] for r in unique_search_results}
    new_results = [res for res in sorted_results if res["videoId"] not in existing_ids]
    unique_search_results.extend(new_results)

    return jsonify({"search_results": sorted_results})

@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    """Fetches trending music once per day and caches the results."""
    global cached_trending_music, last_trending_fetch

    # Check if the cache is expired (older than 24 hours)
    if not last_trending_fetch or (datetime.datetime.now() - last_trending_fetch).days >= 1:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&chart=mostPopular&videoCategoryId=10&regionCode=IN&maxResults=30&key={YT_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "items" not in data:
            return jsonify({"error": "Failed to fetch trending music"}), 500

        # Update cache
        cached_trending_music = [
            {
                "videoId": item["id"],
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }
            for item in data["items"]
        ]
        last_trending_fetch = datetime.datetime.now()

    return jsonify({"trending_music": cached_trending_music})

@app.route('/download', methods=['GET'])
def download():
    file_id = request.args.get('file_id', cookies_Extractor.DEFAULT_FILE_ID)
    filename = request.args.get('filename', cookies_Extractor.DEFAULT_FILENAME)

    try:
        saved_path = cookies_Extractor.download_file_from_google_drive(file_id, filename)
        return jsonify({'message': f'File downloaded successfully and saved as: {saved_path}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

# Ensure correct port binding for Railway
PORT = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
