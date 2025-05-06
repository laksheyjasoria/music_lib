# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from config import Config
# from song import Song, SongPool
# from utils.telegram_logger import telegram_handler
# import logging
# import datetime
# import requests
# import audioV3
# import utilsV2
# import cookies_Extractor

# app = Flask(__name__)
# CORS(app)

# # Configure logging
# app.logger.addHandler(telegram_handler)
# app.logger.setLevel(logging.INFO)

# # Initialize song pool and trending cache
# song_pool = SongPool()
# cached_trending_ids = []
# last_trending_fetch = None


# @app.route("/get_audio", methods=["GET"])
# def get_audio():
#     video_id = request.args.get("videoId")
#     if not video_id:
#         return jsonify({"error": "Missing 'videoId' parameter"}), 400

#     song = song_pool.get_song(video_id)
#     if not song:
#         return jsonify({"error": "Song not found"}), 404

#     if not song.audio_url:
#         try:
#             audio_url = audioV3.get_audio_url(video_id)
#             if not audio_url:
#                 raise ValueError("Failed to get audio URL")
#             song.update_audio_url(audio_url)
#         except Exception as e:
#             app.logger.error(f"Audio fetch failed for {video_id}: {str(e)}")
#             return jsonify({"error": str(e)}), 500

#     song.increment_play_count()
#     return jsonify(song.to_dict())


# @app.route("/search_music", methods=["GET"])
# def search_music():
#     query = request.args.get("query")
#     if not query:
#         return jsonify({"error": "Missing 'query' parameter"}), 400

#     try:
#         search_url = f"{Config.YT_API_BASE_URL}/search"
#         params = {
#             "part": "snippet",
#             "type": "video",
#             "videoCategoryId": 10,
#             "regionCode": "IN",
#             "maxResults": 50,
#             "q": query,
#             "key": Config.YT_API_KEY
#         }

#         search_response = requests.get(search_url, params=params)
#         search_response.raise_for_status()
#         search_data = search_response.json()

#         video_ids = [
#             item["id"]["videoId"]
#             for item in search_data.get("items", [])
#             if "videoId" in item.get("id", {})
#         ]

#         if not video_ids:
#             return jsonify({"search_results": []})

#         details_url = f"{Config.YT_API_BASE_URL}/videos"
#         details_params = {
#             "part": "snippet,contentDetails,statistics",
#             "id": ",".join(video_ids),
#             "key": Config.YT_API_KEY
#         }

#         details_response = requests.get(details_url, params=details_params)
#         details_response.raise_for_status()
#         details_data = details_response.json()

#         new_songs = []
#         for item in details_data.get("items", []):
#             try:
#                 video_id = item["id"]
#                 if song_pool.get_song(video_id):
#                     continue
#                 title=item["snippet"]["title"]
#                 duration=utilsV2.iso8601_to_seconds(item["contentDetails"]["duration"])
#                 if not utilsV2.is_valid(title,duration):
#                     continue
                    
#                 song = Song(
#                     video_id=video_id,
#                     title=title,
#                     thumbnail=item["snippet"]["thumbnails"]["high"]["url"],
#                     duration=duration
#                 )

#                 if song.is_valid() and song_pool.add_song(song):
#                     new_songs.append(song)

#             except Exception as e:
#                 app.logger.warning(f"Error processing video {video_id}: {str(e)}")

#         sorted_songs = sorted(new_songs, key=lambda s: s.duration)
#         return jsonify({"search_results": [s.to_dict() for s in sorted_songs]})

#     except requests.RequestException as e:
#         app.logger.error(f"YouTube API error: {str(e)}")
#         return jsonify({"error": "YouTube API failure"}), 500


# @app.route("/get_trending_music", methods=["GET"])
# def get_trending_music():
#     global cached_trending_ids, last_trending_fetch

#     try:
#         if not last_trending_fetch or (
#             datetime.datetime.now() - last_trending_fetch
#         ) >= Config.TRENDING_CACHE_TTL:
#             url = f"{Config.YT_API_BASE_URL}/videos"
#             params = {
#                 "part": "snippet,contentDetails",
#                 "chart": "mostPopular",
#                 "videoCategoryId": 10,
#                 "regionCode": "IN",
#                 "maxResults": Config.MAX_TRENDING_RESULTS,
#                 "key": Config.YT_API_KEY
#             }

#             response = requests.get(url, params=params)
#             response.raise_for_status()
#             data = response.json()

#             new_trending_ids = [item["id"] for item in data["items"]]

#             for item in data["items"]:
#                 try:
#                     video_id = item["id"]
#                     title=item["snippet"]["title"]
#                     duration=utilsV2.iso8601_to_seconds(item["contentDetails"]["duration"])
#                     if not utilsV2.is_valid(title,duration):
#                         continue
                        
#                     if not song_pool.get_song(video_id):
#                         song = Song(
#                             video_id=video_id,
#                             title=title,
#                             thumbnail=item["snippet"]["thumbnails"]["high"]["url"],
#                             duration=duration
#                         )
#                         song_pool.add_song(song)
#                 except Exception as e:
#                     app.logger.warning(f"Error processing trending video {video_id}: {str(e)}")

#             cached_trending_ids = new_trending_ids
#             last_trending_fetch = datetime.datetime.now()

#         trending_songs = song_pool.get_songs_by_ids(cached_trending_ids)
#         return jsonify({"trending_music": [s.to_dict() for s in trending_songs]})

#     except requests.RequestException as e:
#         app.logger.error(f"Trending music fetch failed: {str(e)}")
#         return jsonify({"error": "Failed to fetch trending music"}), 500


# @app.route("/get_most_played_songs", methods=["GET"])
# def get_most_played_songs():
#     all_songs = song_pool.get_all_songs()
#     played_songs = [s for s in all_songs if s.play_count > 0]
#     sorted_songs = sorted(played_songs, key=lambda s: s.play_count, reverse=True)[:Config.MAX_PLAY_COUNTS]
#     return jsonify({"most_played_songs": [s.to_dict() for s in sorted_songs]})


# @app.route("/download", methods=["GET"])
# def download():
#     file_id = request.args.get("file_id", cookies_Extractor.DEFAULT_FILE_ID)
#     filename = request.args.get("filename", cookies_Extractor.DEFAULT_FILENAME)

#     try:
#         saved_path = cookies_Extractor.download_file_from_google_drive(file_id, filename)
#         return jsonify({"message": f"File downloaded successfully: {saved_path}"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)

from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from song import Song, SongPool
from utils.telegram_logger import telegram_handler
import logging
import datetime
import requests
import audioV3
import utilsV2
import cookies_Extractor

app = Flask(__name__)
CORS(app)

# Configure logging
app.logger.addHandler(telegram_handler)
app.logger.setLevel(logging.INFO)

# Initialize song pool and trending cache
song_pool = SongPool()
cached_trending_ids = []
last_trending_fetch = None


@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing 'videoId' parameter"}), 400

    song = song_pool.get_song(video_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404

    if not song.audio_url:
        try:
            audio_url = audioV3.get_audio_url(video_id)
            if not audio_url:
                raise ValueError("Failed to get audio URL")
            song.update_audio_url(audio_url)
        except Exception as e:
            app.logger.error(f"Audio fetch failed for {video_id}: {e}")
            return jsonify({"error": str(e)}), 500

    song.increment_play_count()
    return jsonify(song.to_dict())


@app.route("/search_music", methods=["GET"])
def search_music():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    try:
        # Search for video IDs
        resp = requests.get(
            f"{Config.YT_API_BASE_URL}/search",
            params={
                "part": "snippet",
                "type": "video",
                "videoCategoryId": 10,
                "regionCode": "IN",
                "maxResults": 50,
                "q": query,
                "key": Config.YT_API_KEY
            },
        )
        resp.raise_for_status()
        items = resp.json().get("items", [])

        video_ids = [i["id"]["videoId"] for i in items if "videoId" in i.get("id", {})]
        if not video_ids:
            return jsonify({"search_results": []})

        # Fetch details for each video ID
        resp2 = requests.get(
            f"{Config.YT_API_BASE_URL}/videos",
            params={
                "part": "snippet,contentDetails,statistics",
                "id": ",".join(video_ids),
                "key": Config.YT_API_KEY
            },
        )
        resp2.raise_for_status()
        details = resp2.json().get("items", [])

        new_songs = []
        for info in details:
            try:
                vid = info["id"]
                if song_pool.get_song(vid):
                    continue

                title = info["snippet"]["title"]
                dur = utilsV2.iso8601_to_seconds(info["contentDetails"]["duration"])
                # Validate with utilsV2 before creating Song
                if not utilsV2.is_valid(title, dur):
                    continue

                song = Song(
                    video_id=vid,
                    title=title,
                    thumbnail=info["snippet"]["thumbnails"]["high"]["url"],
                    duration=dur
                )

                if song_pool.add_song(song):
                    new_songs.append(song)
            except Exception as e:
                app.logger.warning(f"Error processing video {vid}: {e}")

        # Sort by duration and return
        new_songs.sort(key=lambda s: s.duration)
        return jsonify({"search_results": [s.to_dict() for s in new_songs]})

    except requests.RequestException as e:
        app.logger.error(f"YouTube API error: {e}")
        return jsonify({"error": "YouTube API failure"}), 500


@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    global cached_trending_ids, last_trending_fetch

    try:
        stale = not last_trending_fetch or (datetime.datetime.now() - last_trending_fetch) >= Config.TRENDING_CACHE_TTL
        if stale:
            resp = requests.get(
                f"{Config.YT_API_BASE_URL}/videos",
                params={
                    "part": "snippet,contentDetails",
                    "chart": "mostPopular",
                    "videoCategoryId": 10,
                    "regionCode": "IN",
                    "maxResults": Config.MAX_TRENDING_RESULTS,
                    "key": Config.YT_API_KEY
                },
            )
            resp.raise_for_status()
            data = resp.json().get("items", [])

            ids = []
            for info in data:
                vid = info["id"]
                title = info["snippet"]["title"]
                dur = utilsV2.iso8601_to_seconds(info["contentDetails"]["duration"])
                # Validate before Song creation
                if not utilsV2.is_valid(title, dur):
                    continue

                song = Song(video_id=vid, title=title, thumbnail=info["snippet"]["thumbnails"]["high"]["url"], duration=dur)
                if song_pool.add_song(song):
                    ids.append(vid)

            cached_trending_ids = ids
            last_trending_fetch = datetime.datetime.now()

        trending = song_pool.get_songs_by_ids(cached_trending_ids)
        return jsonify({"trending_music": [s.to_dict() for s in trending]})
    except requests.RequestException as e:
        app.logger.error(f"Trending fetch failed: {e}")
        return jsonify({"error": "Failed to fetch trending music"}), 500


@app.route("/get_most_played_songs", methods=["GET"])
def get_most_played_songs():
    all_s = song_pool.get_all_songs()
    played = [s for s in all_s if s.play_count > 0]
    played.sort(key=lambda s: s.play_count, reverse=True)
    top = played[: Config.MAX_PLAY_COUNTS]
    return jsonify({"most_played_songs": [s.to_dict() for s in top]})


@app.route("/download", methods=["GET"])
def download():
    file_id = request.args.get("file_id", cookies_Extractor.DEFAULT_FILE_ID)
    filename = request.args.get("filename", cookies_Extractor.DEFAULT_FILENAME)
    try:
        path = cookies_Extractor.download_file_from_google_drive(file_id, filename)
        return jsonify({"message": f"File downloaded successfully: {path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
