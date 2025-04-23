import re
import json
def iso8601_to_seconds(duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return 0
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds

def convert_to_ytdlp_cookies(input_json):
    """
    Convert cookies from a JSON format into the format yt-dlp expects.
    
    :param input_json: Original cookies in JSON format.
    :return: A list of dictionaries formatted for yt-dlp.
    """
    cookies_for_ytdlp = []
    
    for cookie in input_json:
        # Convert the cookie data to the format yt-dlp expects
        ytdlp_cookie = {
            "domain": cookie.get("domain"),
            "expirationDate": cookie.get("expirationDate"),
            "hostOnly": cookie.get("hostOnly"),
            "httpOnly": cookie.get("httpOnly"),
            "name": cookie.get("name"),
            "path": cookie.get("path"),
            "sameSite": cookie.get("sameSite"),
            "secure": cookie.get("secure"),
            "session": cookie.get("session"),
            "storeId": cookie.get("storeId"),
            "value": cookie.get("value"),
            "id": cookie.get("id")
        }
        cookies_for_ytdlp.append(ytdlp_cookie)
    
    return cookies_for_ytdlp
