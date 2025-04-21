import os
import requests
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List

# ─── 1) Grab your YouTube API key from env ─────────────────────────────────────
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise RuntimeError("Please set YOUTUBE_API_KEY in your environment")

app = FastAPI(title="YouTube‑based Top Genre Singers")

# ─── 2) Response model ────────────────────────────────────────────────────────
class Singer(BaseModel):
    name: str
    image_url: str

# ─── 3) Endpoint ─────────────────────────────────────────────────────────────
@app.get("/top-singers", response_model=List[Singer])
def top_singers(
    genre: str = Query(..., description="Genre to search, e.g. bollywood, punjabi…"),
    limit: int = Query(5, ge=1, le=20, description="Max number of channels to return")
):
    """
    Searches YouTube for channels named “<genre> singer” and returns
    channel title + thumbnail image URL.
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part":      "snippet",
        "q":         f"{genre} singer",
        "type":      "channel",
        "maxResults": limit,
        "key":       YOUTUBE_API_KEY,
    }
    r = requests.get(url, params=params, timeout=5)
    if r.status_code != 200:
        raise HTTPException(502, f"YouTube API error {r.status_code}")
    data = r.json()
    items = data.get("items", [])
    singers = []
    for it in items:
        snip = it["snippet"]
        title = snip["channelTitle"]
        # pick the best thumbnail we have
        thumbs = snip.get("thumbnails", {})
        img = (
            thumbs.get("high"  ,{}).get("url") or 
            thumbs.get("medium",{}).get("url") or
            thumbs.get("default",{}).get("url","")
        )
        singers.append(Singer(name=title, image_url=img))
    return singers
