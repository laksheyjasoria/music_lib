# import os
# import requests
# from fastapi import FastAPI, HTTPException, Query
# from pydantic import BaseModel
# from typing import List

# # ─── 1) Grab your YouTube API key from env ─────────────────────────────────────
# YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
# if not YOUTUBE_API_KEY:
#     raise RuntimeError("Please set YOUTUBE_API_KEY in your environment")

# app = FastAPI(title="YouTube‑based Top Genre Singers")

# # ─── 2) Response model ────────────────────────────────────────────────────────
# class Singer(BaseModel):
#     name: str
#     image_url: str

# # ─── 3) Endpoint ─────────────────────────────────────────────────────────────
# @app.get("/top-singers", response_model=List[Singer])
# def top_singers(
#     genre: str = Query(..., description="Genre to search, e.g. bollywood, punjabi…"),
#     limit: int = Query(5, ge=1, le=20, description="Max number of channels to return")
# ):
#     """
#     Searches YouTube for channels named “<genre> singer” and returns
#     channel title + thumbnail image URL.
#     """
#     url = "https://www.googleapis.com/youtube/v3/search"
#     params = {
#         "part":      "snippet",
#         "q":         f"{genre} singer",
#         "type":      "channel",
#         "maxResults": limit,
#         "key":       YOUTUBE_API_KEY,
#     }
#     r = requests.get(url, params=params, timeout=5)
#     if r.status_code != 200:
#         raise HTTPException(502, f"YouTube API error {r.status_code}")
#     data = r.json()
#     items = data.get("items", [])
#     singers = []
#     for it in items:
#         snip = it["snippet"]
#         title = snip["channelTitle"]
#         # pick the best thumbnail we have
#         thumbs = snip.get("thumbnails", {})
#         img = (
#             thumbs.get("high"  ,{}).get("url") or 
#             thumbs.get("medium",{}).get("url") or
#             thumbs.get("default",{}).get("url","")
#         )
#         singers.append(Singer(name=title, image_url=img))
#     return singers

import os
import logging
from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
import httpx
from functools import lru_cache

# ─── Setup ──────────────────────────────────────────────────────────────────
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise RuntimeError("Missing YOUTUBE_API_KEY environment variable")

app = FastAPI(
    title="YouTube Genre Singers API",
    description="Discover top music artists by genre through YouTube channels",
    version="1.1.0"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Models ──────────────────────────────────────────────────────────────────
class Singer(BaseModel):
    name: str
    channel_id: str
    image_url: str
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Arijit Singh",
                "channel_id": "UC4wW6Q0kY3B7kU5PwD6J1Zw",
                "image_url": "https://yt3.ggpht.com/.../photo.jpg",
                "description": "Official YouTube Channel of Arijit Singh"
            }
        }

# ─── Services ───────────────────────────────────────────────────────────────
async def get_youtube_client():
    async with httpx.AsyncClient(timeout=10) as client:
        yield client

# ─── Core Logic ─────────────────────────────────────────────────────────────
@app.get("/top-singers", response_model=List[Singer])
async def get_top_singers(
    genre: str = Query(..., min_length=2, max_length=50,
                      example="bollywood",
                      description="Music genre to search (e.g. pop, rock, punjabi)"),
    limit: int = Query(5, ge=1, le=20,
                      description="Number of results to return (1-20)"),
    client: httpx.AsyncClient = Depends(get_youtube_client)
):
    """
    Discover top YouTube channels for a specific music genre.
    Returns channels with metadata sorted by relevance.
    """
    try:
        # Cache repeated identical requests
        return await _fetch_cached_results(genre, limit, client)
    except httpx.HTTPStatusError as e:
        logger.error(f"YouTube API error: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"YouTube API responded with error: {e.response.status_code}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@lru_cache(maxsize=100)
async def _fetch_cached_results(genre: str, limit: int, client: httpx.AsyncClient):
    """Cached API call handler with request validation"""
    params = {
        "part": "snippet",
        "q": f"{genre.strip().lower()} singer",
        "type": "channel",
        "maxResults": limit,
        "key": YOUTUBE_API_KEY,
        "order": "relevance"
    }
    
    response = await client.get(
        "https://www.googleapis.com/youtube/v3/search",
        params=params
    )
    response.raise_for_status()
    
    return [
        Singer(
            name=item["snippet"]["channelTitle"],
            channel_id=item["id"]["channelId"],
            image_url=_best_thumbnail(item["snippet"].get("thumbnails", {})),
            description=item["snippet"].get("description")
        ) for item in response.json().get("items", [])
    ]

def _best_thumbnail(thumbnails: dict) -> str:
    """Select highest quality available thumbnail"""
    for quality in ["high", "medium", "default"]:
        if thumbnails.get(quality):
            return thumbnails[quality]["url"]
    return ""
