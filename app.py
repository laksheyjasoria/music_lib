# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import logging
# import threading
# import time
# from datetime import datetime

# from config.config import Config
# from core.song_pool import SongPool
# from core.song import Song
# from services.google_drive import GoogleDriveSync
# from services.telegram_bot import CookieRefresherBot
# from utils.logger import setup_logger
# from utils.cookie_utils import download_file_from_google_drive, convert_cookies_to_ytdlp_format
# from utils.duration_parser import iso8601_to_seconds
# from utils.validation import is_valid_song

# app = Flask(__name__)
# CORS(app)
# logger = setup_logger(__name__)

# # Initialize services
# try:
#     drive_sync = GoogleDriveSync()
#     if not drive_sync.drive_enabled:
#         logger.warning("Google Drive synchronization disabled")
# except Exception as e:
#     logger.error(f"Failed to initialize Google Drive sync: {str(e)}")
#     drive_sync = None

# song_pool = SongPool()
# cached_trending_ids = []
# last_trending_fetch = None

# @app.route("/health")
# def health_check():
#     return "OK", 200

# @app.route("/get_audio", methods=["GET"])
# def get_audio():
#     video_id = request.args.get("videoId")
#     if not video_id:
#         return jsonify({"error": "Missing videoId parameter"}), 400

#     song = song_pool.get_song(video_id)
#     if not song:
#         try:
#             song = Song.from_video_id(video_id)
#             song_pool.add_song(song)
#         except ValueError as e:
#             return jsonify({"error": str(e)}), 400

#     if not song.audio_url:
#         from core.audio_fetcher import audio_fetcher
#         audio_url = audio_fetcher.get_audio_url(video_id)
#         if not audio_url:
#             return jsonify({"error": "Failed to get audio URL"}), 500
#         song.update_audio_url(audio_url)

#     return jsonify(song.to_dict())


# @app.route("/search_music", methods=["GET"])
# def search_music():
#     query = request.args.get("query")
#     if not query:
#         return jsonify({"error": "Missing 'query' parameter"}), 400

#     try:
#         # Search for video IDs
#         resp = requests.get(
#             f"{Config.YT_API_BASE_URL}/search",
#             params={
#                 "part": "snippet",
#                 "type": "video",
#                 "videoCategoryId": 10,
#                 "regionCode": "IN",
#                 "maxResults": 50,
#                 "q": query,
#                 "key": Config.YT_API_KEY
#             },
#         )
#         resp.raise_for_status()
#         items = resp.json().get("items", [])

#         video_ids = [i["id"]["videoId"] for i in items if "videoId" in i.get("id", {})]
#         if not video_ids:
#             return jsonify({"search_results": []})

#         # Fetch details for each video ID
#         resp2 = requests.get(
#             f"{Config.YT_API_BASE_URL}/videos",
#             params={
#                 "part": "snippet,contentDetails,statistics",
#                 "id": ",".join(video_ids),
#                 "key": Config.YT_API_KEY
#             },
#         )
#         resp2.raise_for_status()
#         details = resp2.json().get("items", [])

#         new_songs = []
#         for info in details:
#             try:
#                 vid = info["id"]
#                 if song_pool.get_song(vid):
#                     continue

#                 title = info["snippet"]["title"]
#                 dur = utilsV2.iso8601_to_seconds(info["contentDetails"]["duration"])
#                 # Validate with utilsV2 before creating Song
#                 if not utilsV2.is_valid(title, dur):
#                     continue

#                 song = Song(
#                     video_id=vid,
#                     title=title,
#                     thumbnail=info["snippet"]["thumbnails"]["high"]["url"],
#                     duration=dur
#                 )

#                 if song_pool.add_song(song):
#                     new_songs.append(song)
#             except Exception as e:
#                 app.logger.warning(f"Error processing video {vid}: {e}")

#         # Sort by duration and return
#         new_songs.sort(key=lambda s: s.duration)
#         return jsonify({"search_results": [s.to_dict() for s in new_songs]})

#     except requests.RequestException as e:
#         app.logger.error(f"YouTube API error: {e}")
#         return jsonify({"error": "YouTube API failure"}), 500

# @app.route("/track_play", methods=["POST"])
# def track_play():
#     video_id = request.json.get("videoId")
#     if not video_id:
#         return jsonify({"error": "Missing videoId in request body"}), 400
    
#     song = song_pool.get_song(video_id)
#     if not song:
#         return jsonify({"error": "Song not found"}), 404
    
#     try:
#         song.increment_play_count()
#         return jsonify({
#             "status": "success",
#             "videoId": video_id,
#             "newCount": song.play_count
#         })
#     except Exception as e:
#         app.logger.error(f"Count increment failed for {video_id}: {e}")
#         return jsonify({"error": "Internal server error"}), 500

# @app.route("/get_all_songs", methods=["GET"])
# def get_all_songs():
#     all_songs = song_pool.get_all_songs()
#     return jsonify([song.to_dict() for song in all_songs])

# @app.route("/get_trending_music", methods=["GET"])
# def get_trending_music():
#     global cached_trending_ids, last_trending_fetch

#     try:
#         stale = not last_trending_fetch or (datetime.datetime.now() - last_trending_fetch) >= Config.TRENDING_CACHE_TTL
#         if stale:
#             resp = requests.get(
#                 f"{Config.YT_API_BASE_URL}/videos",
#                 params={
#                     "part": "snippet,contentDetails",
#                     "chart": "mostPopular",
#                     "videoCategoryId": 10,
#                     "regionCode": "IN",
#                     "maxResults": Config.MAX_TRENDING_RESULTS,
#                     "key": Config.YT_API_KEY
#                 },
#             )
#             resp.raise_for_status()
#             data = resp.json().get("items", [])

#             ids = []
#             for info in data:
#                 vid = info["id"]
#                 title = info["snippet"]["title"]
#                 dur = utilsV2.iso8601_to_seconds(info["contentDetails"]["duration"])
#                 # Validate before Song creation
#                 if not utilsV2.is_valid(title, dur):
#                     continue

#                 song = Song(video_id=vid, title=title, thumbnail=info["snippet"]["thumbnails"]["high"]["url"], duration=dur)
#                 if song_pool.add_song(song):
#                     ids.append(vid)

#             cached_trending_ids = ids
#             last_trending_fetch = datetime.datetime.now()

#         trending = song_pool.get_songs_by_ids(cached_trending_ids)
#         return jsonify({"trending_music": [s.to_dict() for s in trending]})
#     except requests.RequestException as e:
#         app.logger.error(f"Trending fetch failed: {e}")
#         return jsonify({"error": "Failed to fetch trending music"}), 500


# @app.route("/get_most_played_songs", methods=["GET"])
# def get_most_played_songs():
#     all_s = song_pool.get_all_songs()
#     played = [s for s in all_s if s.play_count > 0]
#     played.sort(key=lambda s: s.play_count, reverse=True)
#     top = played[: Config.MAX_PLAY_COUNTS]
#     return jsonify({"most_played_songs": [s.to_dict() for s in top]})


# @app.route("/refresh_cookies", methods=["GET"])
# def download():
#     file_id = request.args.get("file_id", cookies_Extractor.DEFAULT_FILE_ID)
#     filename = request.args.get("filename", cookies_Extractor.DEFAULT_FILENAME)
#     try:
#         path = cookies_Extractor.download_file_from_google_drive(file_id, filename)
#         utilsV2.convert_cookies_to_ytdlp_format()
#         return jsonify({"message": f"File downloaded successfully: {path}"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # @app.route("/refresh", methods=["GET"])
# # def refresh():
# #     file_id = request.args.get("file_id", cookies_Extractor.DEFAULT_FILE_ID)
# #     filename = request.args.get("filename", cookies_Extractor.DEFAULT_FILENAME)
# #     try:
# #         # 1) Do your download
# #         path = cookies_Extractor.download_file_from_google_drive(file_id, filename)

# #         # 2) Trigger redeploy
# #         result = redeployer.trigger()
# #         status = 200 if result.get("status") == "ok" else 500
# #         return jsonify(result), status

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500
      
# @app.route("/get_song", methods=["GET"])
# def get_song():
#     video_id = request.args.get("videoId")
#     if not video_id:
#         return jsonify({"error": "Missing videoId parameter"}), 400

#     song = song_pool.get_song(video_id)
#     if not song:
#         return jsonify({"error": f"No song found with videoId '{video_id}'"}), 404

#     return jsonify(song.to_dict())

# def wait_for_flask_startup():
#     """Poll the Flask server until it's up."""
#     url = f"http://localhost:{Config.PORT}/health"  # Use an actual lightweight endpoint
#     for _ in range(10):
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 return True
#         except requests.exceptions.ConnectionError:
#             pass
#         time.sleep(2)
#     return False

# def start_telegram_bot():
#     if not Config.TELEGRAM_BOT_TOKEN:
#         logger.warning("Telegram bot token not configured")
#         return

#     bot = CookieRefresherBot(Config.TELEGRAM_BOT_TOKEN, song_pool)
#     bot.run()

# def background_sync():
#     while True:
#         try:
#             if drive_sync and drive_sync.drive_enabled:
#                 success = drive_sync.bidirectional_sync(song_pool)
#                 logger.info(f"Drive sync {'succeeded' if success else 'failed'}")
#             time.sleep(Config.SYNC_INTERVAL)
#         except Exception as e:
#             logger.error(f"Background sync error: {e}")
#             time.sleep(60)

# if __name__ == "__main__":
#     # Initial sync
#     if drive_sync and drive_sync.drive_enabled:
#         drive_sync.bidirectional_sync(song_pool)

#     # Start background threads
#     threading.Thread(target=start_telegram_bot, daemon=True).start()
#     threading.Thread(target=background_sync, daemon=True).start()

#     app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import threading
import time
import requests
from datetime import datetime
import socket
import os
import sys
from waitress import serve
import atexit

from config.config import Config
from core.song_pool import SongPool
from core.song import Song
from services.google_drive import GoogleDriveSync
from services.telegram_bot import CookieRefresherBot
from utils.logger import setup_logger
from utils.cookie_utils import download_file_from_google_drive, convert_cookies_to_ytdlp_format,download_file_from_google_drive_token
from utils.duration_parser import iso8601_to_seconds
from utils.validation import is_valid_song
from drive_sync import DriveSongPoolSync

app = Flask(__name__)
CORS(app)
logger = setup_logger(__name__)

# Initialize services
try:
    drive_sync = GoogleDriveSync()
    if not drive_sync.drive_enabled:
        logger.warning("Google Drive synchronization disabled")
except Exception as e:
    logger.error(f"Failed to initialize Google Drive sync: {str(e)}")
    drive_sync = None

song_pool = SongPool()
cached_trending_ids = []
last_trending_fetch = None

@app.route("/health")
def health_check():
    return "OK", 200

@app.route("/get_audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing videoId parameter"}), 400

    song = song_pool.get_song(video_id)
    if not song:
        try:
            song = Song.from_video_id(video_id)
            song_pool.add_song(song)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    if not song.audio_url:
        from core.audio_fetcher import audio_fetcher
        audio_url = audio_fetcher.get_audio_url(video_id)
        if not audio_url:
            return jsonify({"error": "Failed to get audio URL"}), 500
        song.update_audio_url(audio_url)

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
                dur = iso8601_to_seconds(info["contentDetails"]["duration"])
                if not is_valid_song(title, dur):
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
                logger.warning(f"Error processing video {vid}: {e}")

        # Sort by duration and return
        new_songs.sort(key=lambda s: s.duration)
        return jsonify({"search_results": [s.to_dict() for s in new_songs]})

    except requests.RequestException as e:
        logger.error(f"YouTube API error: {e}")
        return jsonify({"error": "YouTube API failure"}), 500

@app.route("/track_play", methods=["POST"])
def track_play():
    video_id = request.json.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing videoId in request body"}), 400
    
    song = song_pool.get_song(video_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404
    
    try:
        song.increment_play_count()
        return jsonify({
            "status": "success",
            "videoId": video_id,
            "newCount": song.play_count
        })
    except Exception as e:
        logger.error(f"Count increment failed for {video_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/get_all_songs", methods=["GET"])
def get_all_songs():
    all_songs = song_pool.get_all_songs()
    return jsonify([song.to_dict() for song in all_songs])

@app.route("/get_trending_music", methods=["GET"])
def get_trending_music():
    global cached_trending_ids, last_trending_fetch

    try:
        stale = not last_trending_fetch or (datetime.now() - last_trending_fetch) >= Config.TRENDING_CACHE_TTL
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
                dur = iso8601_to_seconds(info["contentDetails"]["duration"])
                if not is_valid_song(title, dur):
                    continue

                song = Song(video_id=vid, title=title, thumbnail=info["snippet"]["thumbnails"]["high"]["url"], duration=dur)
                if song_pool.add_song(song):
                    ids.append(vid)

            cached_trending_ids = ids
            last_trending_fetch = datetime.now()

        trending = song_pool.get_songs_by_ids(cached_trending_ids)
        return jsonify({"trending_music": [s.to_dict() for s in trending]})
    except requests.RequestException as e:
        logger.error(f"Trending fetch failed: {e}")
        return jsonify({"error": "Failed to fetch trending music"}), 500

@app.route("/get_most_played_songs", methods=["GET"])
def get_most_played_songs():
    all_s = song_pool.get_all_songs()
    played = [s for s in all_s if s.play_count > 0]
    played.sort(key=lambda s: s.play_count, reverse=True)
    top = played[:Config.MAX_PLAY_COUNTS]
    return jsonify({"most_played_songs": [s.to_dict() for s in top]})

@app.route("/refresh_cookies", methods=["GET"])
def refresh_cookies():
    try:
        path = download_file_from_google_drive()
        convert_cookies_to_ytdlp_format()
        return jsonify({"message": f"Cookies refreshed successfully: {path}"})
    except Exception as e:
        logger.error(f"Cookie refresh failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/get_song", methods=["GET"])
def get_song():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing videoId parameter"}), 400

    song = song_pool.get_song(video_id)
    if not song:
        return jsonify({"error": f"No song found with videoId '{video_id}'"}), 404

    return jsonify(song.to_dict())

def start_telegram_bot():
    if not Config.TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram bot token not configured")
        return

    bot = CookieRefresherBot(Config.TELEGRAM_BOT_TOKEN, song_pool)
    bot.run()

# def is_server_responding():
#     try:
#         with socket.create_connection(("0.0.0.0", 5000), timeout=2):
#             return True
#     except (socket.timeout, ConnectionRefusedError):
#         return False

def is_server_responding():
    try:
        response = requests.get(f"http://127.0.0.1:{Config.PORT}/health", timeout=2)
        return response.status_code == 200 and response.text.strip() == "OK"
    except requests.exceptions.RequestException:
        return False

def keep_alive_pinger():
    """Separate thread to ping server externally"""
    while True:
        try:
            # Ping through actual HTTP endpoint
            requests.get(f"http://0.0.0.0:{Config.PORT}/health", timeout=5)
        except Exception as e:
            logger.debug(f"Keep-alive ping failed: {str(e)}")
        time.sleep(30)  # Ping every 30 seconds

def health_monitor():
    """Enhanced health monitor with cooldown"""
    last_restart = time.time()
    restart_cooldown = 300  # 5 minutes between restarts
    
    while True:
        if not is_server_responding():
            if time.time() - last_restart > restart_cooldown:
                logger.critical("Server not responding! Attempting restart...")
                # Graceful restart with process separation
                python = sys.executable
                os.execl(python, python, *sys.argv)
                last_restart = time.time()
            else:
                logger.warning("Server down but in cooldown period")
        time.sleep(15)

def background_sync():
    while True:
        try:
            if drive_sync and drive_sync.drive_enabled:
                success = drive_sync.bidirectional_sync(song_pool)
                logger.info(f"Drive sync {'succeeded' if success else 'failed'}")
            time.sleep(Config.SYNC_INTERVAL)
        except Exception as e:
            logger.error(f"Background sync error: {e}")
            time.sleep(60)

if __name__ == "__main__":

#     try:
#         path = download_file_from_google_drive()
#         convert_cookies_to_ytdlp_format()
#         logger.info({"message": f"Cookies refreshed successfully: {path}"})
#     except Exception as e:
#         logger.error(f"Cookie refresh failed: {e}")
    
#     # # Initial sync
#     # if drive_sync and drive_sync.drive_enabled:
#     #     drive_sync.bidirectional_sync(song_pool)

#     # # Start background threads
#     # threading.Thread(target=start_telegram_bot, daemon=True).start()
#     # threading.Thread(target=background_sync, daemon=True).start()

#     # drive_sync = DriveSongPoolSync(file_id=Config.SONG_POOL_ID)
#     # drive_sync.sync_every_hour()
#     drive_sync = DriveSongPoolSync(file_id=Config.SONG_POOL_ID)
#     drive_sync.sync_every_hour(song_pool)
#     threading.Thread(target=health_monitor, daemon=True).start()
#     app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
    try:
        path = download_file_from_google_drive()
        convert_cookies_to_ytdlp_format()
        logger.info(f"Cookies refreshed successfully: {path}")
    except Exception as e:
        logger.error(f"Cookie refresh failed: {e}")

    # Start all maintenance threads
    # threads = [
    #     # threading.Thread(target=health_monitor, daemon=True),
    #     # threading.Thread(target=keep_alive_pinger, daemon=True),
    #     threading.Thread(target=drive_sync.sync_every_hour, args=(song_pool,), daemon=True)
    # ]
    
    # for t in threads:
    #     t.start()

    # Production server configuration
    logger.info(f"Starting server on port {Config.PORT}")
    serve(app, host="0.0.0.0", port=Config.PORT, threads=4)

    # Cleanup on exit
    atexit.register(lambda: logger.info("Server shutting down"))
