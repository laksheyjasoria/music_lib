import re
import json
import http.cookiejar
def iso8601_to_seconds(duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return 0
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds


def convert_cookies_to_ytdlp_format(json_path='cookies.json', output_path='cookies.txt'):
    """
    Converts a JSON cookies file into a Netscape format cookies file for yt-dlp.
    
    Args:
        json_path (str): Path to the input JSON cookies file.
        output_path (str): Path to save the converted cookies file.
    
    Returns:
        str: Path to the generated cookies file.
    """
    # Load JSON cookies
    with open(json_path, 'r') as f:
        cookies = json.load(f)
    
    # Initialize MozillaCookieJar to handle Netscape format
    cookie_jar = http.cookiejar.MozillaCookieJar(output_path)
    
    for cookie_data in cookies:
        # Convert expiration date to integer (yt-dlp expects Unix timestamp)
        expires = int(cookie_data['expirationDate']) if not cookie_data.get('session', False) else None
        
        # Create a Cookie object
        cookie = http.cookiejar.Cookie(
            version=0,
            name=cookie_data['name'],
            value=cookie_data['value'],
            port=None,
            port_specified=False,
            domain=cookie_data['domain'],
            domain_specified=True,
            domain_initial_dot=cookie_data['domain'].startswith('.'),
            path=cookie_data['path'],
            path_specified=bool(cookie_data['path']),
            secure=cookie_data['secure'],
            expires=expires,
            discard=False,
            comment=None,
            comment_url=None,
            rest={'HttpOnly': cookie_data['httpOnly']},  # Not used in file but included for completeness
            rfc2109=False
        )
        cookie_jar.set_cookie(cookie)
    
    # Save cookies to file (ignore expiration/discard rules)
    cookie_jar.save(ignore_discard=True, ignore_expires=True)
    return output_path

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
    
def is_valid(title,duration) -> bool:
        excluded = {"lofi", "slowed", "reverb", "nightcore","remix","dj remix","djremix","d.j remix","d.j. remix","dj mix","djmix","d.j mix","d.j. mix"}
        t = title.lower()
        return 90 <= duration <= 1200 and not any(k in t for k in excluded)
