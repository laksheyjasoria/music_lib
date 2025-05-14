# # import threading
# # from typing import Optional, List

# # class Song:
# #     def __init__(self, video_id: str, title: str, thumbnail: str, 
# #                  duration: int = 0, popularity: int = 0):
# #         self.video_id = video_id
# #         self.title = title
# #         self.thumbnail = thumbnail
# #         self.duration = duration
# #         self.play_count = 0
# #         self.audio_url: Optional[str] = None
# #         self.popularity = popularity
# #         self._validate_input()

# #     def _validate_input(self):
# #         if not self.video_id:
# #             raise ValueError("Missing video ID")
# #         if not self.title:
# #             raise ValueError("Missing title")
# #         if not self.thumbnail:
# #             raise ValueError("Missing thumbnail")

# #     def is_valid(self):
# #         excluded_keywords = {"lofi", "slowed", "reverb", "nightcore"}
# #         return (
# #             self.duration >= 90 and
# #             self.duration <= 1200 and
# #             not any(kw in self.title.lower() for kw in excluded_keywords)
# #         )

# #     def increment_play_count(self):
# #         self.play_count += 1

# #     def update_audio_url(self, url: str):
# #         self.audio_url = url

# #     def to_dict(self):
# #         return {
# #             "videoId": self.video_id,
# #             "title": self.title,
# #             "thumbnail": self.thumbnail,
# #             "duration": self.duration,
# #             "playCount": self.play_count,
# #             "audioUrl": self.audio_url,
# #             "popularity": self.popularity
# #         }

# # class SongPool:
# #     def __init__(self):
# #         self._songs = {}
# #         self._lock = threading.Lock()

# #     def add_song(self, song: Song) -> bool:
# #         with self._lock:
# #             if song.video_id not in self._songs:
# #                 self._songs[song.video_id] = song
# #                 return True
# #             return False

# #     def get_song(self, video_id: str) -> Optional[Song]:
# #         with self._lock:
# #             return self._songs.get(video_id)

# #     def get_songs_by_ids(self, video_ids: List[str]) -> List[Song]:
# #         with self._lock:
# #             return [self._songs[vid] for vid in video_ids if vid in self._songs]

# #     def get_all_songs(self) -> List[Song]:
# #         with self._lock:
# #             return list(self._songs.values())

# # import threading
# # from typing import Optional, List
# # import re

# # _PHRASES = [
# #     r"official\s+(video|song|audio|lyrics?)", 
# #     r"\b(ft\.?|feat\.?|prod\.?|remix|version|mix)\b.*",
# #     r"\b(hd|4k|mp3|viral|lyrical|dance performance)\b",
# #     r"\b(new|latest)\s+(haryanvi|punjabi|rajasthani)\s+songs?\b.*\d{4}",
# #     r"\bvyrl\b",
# #     r"\b\d{4}\b"
# # ]

# # # Combined patterns for single-pass removal
# # _REMOVAL_PATTERNS = {
# #     "phrases": re.compile(
# #         "|".join(f"({p})" for p in _PHRASES),
# #         flags=re.IGNORECASE | re.UNICODE
# #     ),
# #     "metadata": re.compile(
# #         r"""
# #         [\[\(].*?[\]\)]|      # Brackets/parentheses content
# #         [@#]\w+|               # Mentions/hashtags
# #         -\s*\d{4}$|            # Trailing year with hyphen
# #         \s*[|•]\s*.*           # Content after separators
# #         """, 
# #         flags=re.IGNORECASE | re.UNICODE | re.VERBOSE
# #     ),
# #     "cleanup": re.compile(
# #         r"[^\w\u0900-\u097F\u0A00-\u0A7F\s.,!&+'?-]",  # Allow common punctuation
# #         flags=re.UNICODE
# #     )
# # }

# # _TRIM_PATTERN = re.compile(
# #     r"^\W+|\W+$",  # Trim leading/trailing non-word chars
# #     flags=re.UNICODE
# # )

# # class TitleCleaner:
# #     @staticmethod
# #     def clean_title(raw_title: str) -> str:
# #         """Optimized multilingual title cleaner"""
# #         if not raw_title:
# #             return ""

# #         # Phase 1: Remove large chunks
# #         title = _REMOVAL_PATTERNS["phrases"].sub('', raw_title)
# #         title = _REMOVAL_PATTERNS["metadata"].sub('', title)
        
# #         # Phase 2: Cleanup remaining characters
# #         title = _REMOVAL_PATTERNS["cleanup"].sub('', title)
        
# #         # Final processing
# #         title = _TRIM_PATTERN.sub('', title)
# #         title = re.sub(r'\s+', ' ', title).strip()
        
# #         return title or raw_title[:50]  # Fallback to truncated original

# import threading
# import re
# from typing import Optional, List

# _PHRASES = [
#     # Official content variants
#     r"official\s+(video|song|audio|lyrics?)",  
#     r"official\s+.*?song\b",
    
#     # Feature/production tags
#     r"\b(ft\.?|feat\.?|prod\.?|remix|version|mix|dj)\b.*",
    
#     # Quality/format tags
#     r"\b(hd|4k|mp3|viral|lyrical|dance performance|3d audio|non stop|full video|video song|song promo)\b",
    
#     # Regional song patterns
#     r"\b(new|latest|best)\s+(haryanvi|punjabi|rajasthani)(\s*&\s*(haryanvi|punjabi|rajasthani))?\s+songs?\b",
    
#     # Platform references and years
#     r"\bvyrl\b",
#     r"\b\d{4}\b",
    
#     # DJ variations
#     r"\b(d\s?j\.?|dj)\s*song\b",
    
#     # Common redundant phrases
#     r"\boriginal\s+song\b",
#     r"\bnon\s+stop\s+(haryanvi|punjabi|rajasthani)\b",
#     r"\bdance\s+video\b",
#     r"\bfull\s+video\s+with\s+lyrics\b",
#     r"\bbest\s+song\b",
#     r"\b(new|latest)\s+haryanvi\s*&\s*rajasthani\s+song\b",
# ]

# _REMOVAL_PATTERNS = {
#     "phrases": re.compile(
#         "|".join(f"({p})" for p in _PHRASES),
#         flags=re.IGNORECASE | re.UNICODE
#     ),
#     "metadata": re.compile(
#         r"""
#         [\[\(].*?[\]\)]|      # Brackets/parentheses content
#         [@#]\w+|               # Mentions/hashtags
#         -\s*\d{4}$|            # Trailing year with hyphen
#         \s*[|•.]\s*.*          # Content after separators
#         """, 
#         flags=re.IGNORECASE | re.UNICODE | re.VERBOSE
#     ),
#     "cleanup": re.compile(
#         r"[^\w\u0900-\u097F\u0A00-\u0A7F\s.,!&+'?-]",  # Allow common punctuation
#         flags=re.UNICODE
#     )
# }

# _TRIM_PATTERN = re.compile(
#     r"^\W+|\W+$",  # Trim leading/trailing non-word chars
#     flags=re.UNICODE
# )

# class TitleCleaner:
#     @staticmethod
#     def clean_title(raw_title: str) -> str:
#         """Optimized multilingual title cleaner"""
#         if not raw_title:
#             return ""

#         # Phase 1: Remove large chunks
#         title = _REMOVAL_PATTERNS["phrases"].sub('', raw_title)
#         title = _REMOVAL_PATTERNS["metadata"].sub('', title)
        
#         # Phase 2: Cleanup remaining characters
#         title = _REMOVAL_PATTERNS["cleanup"].sub('', title)
        
#         # Final processing
#         title = _TRIM_PATTERN.sub('', title)
#         title = re.sub(r'\s+', ' ', title).strip()
        
#         return title or raw_title[:50]  # Fallback to truncated original
# class Song:
#     def __init__(self, video_id: str, title: str, thumbnail: str, duration: int = 0):
#         self.video_id = video_id
#         self.title = TitleCleaner.clean_title(title)
#         self.thumbnail = thumbnail
#         self.duration = duration
#         self.play_count = 0
#         self.audio_url: Optional[str] = None
#         self._validate_input()

#     def _validate_input(self):
#         if not self.video_id:
#             raise ValueError("Missing video ID")
#         if not self.title:
#             raise ValueError("Missing title")
#         if not self.thumbnail:
#             raise ValueError("Missing thumbnail")

#     def is_valid(self):
#         excluded_keywords = {"lofi", "slowed", "reverb", "nightcore","remix","dj remix","djremix"}
#         return (
#             self.duration >= 90 and
#             self.duration <= 1200 and
#             not any(kw in self.title.lower() for kw in excluded_keywords)
#         )

#     def increment_play_count(self):
#         self.play_count += 1

#     def update_audio_url(self, url: str):
#         self.audio_url = url

#     def to_dict(self):
#         return {
#             "videoId": self.video_id,
#             "title": self.title,
#             "thumbnail": self.thumbnail,
#             "duration": self.duration,
#             "playCount": self.play_count,
#             "audioUrl": self.audio_url
#         }

#     # def clean_title(self, raw_title: str) -> str:
#     #     """Enhanced title cleaner with configurable phrases"""
#     #     # Default phrases to remove if none provided
#     #     phrases = [
#     #         "official video", "lyrics", "video", "hd", "4k", 
#     #         "remix", "version", "ft.", "feat.", "mp3", "official song","official songs","full","full song","full songs","viral song","lyrical song","dance performance","dj viral song","Haryanvi Song","new haryanvi songs haryanavi","new haryanvi songs haryanvi","haryanvi songs haryanavi","new song of","new haryanvi & rajasthani song","viral haryanvi","vyrl haryanvi"
#     #     ]



#     #     cleaned_title = raw_title
        
#     #     # Remove phrases (case-insensitive)
#     #     for phrase in phrases:
#     #         cleaned_title = re.sub(
#     #             r'\s*{}\b'.format(re.escape(phrase)),
#     #             '',
#     #             cleaned_title,
#     #             flags=re.IGNORECASE
#     #         )
        
#     #     # Remove components in parentheses/brackets
#     #     cleaned_title = re.sub(r'[\[\(].*?[\]\)]', '', cleaned_title)
        
#     #     # Remove @mentions and #hashtags
#     #     cleaned_title = re.sub(r'\s*[@#]\w+\b', '', cleaned_title)

#     #     # remove new/latest WORD song/songs yyyy
#     #     # cleaned_title = re.sub(r"\b(latest|new)\s+\w+(?:\s+\w+)?\s+songs?\s*\{?\d{4}\}?", "", cleaned_title, flags=re.IGNORECASE).strip()

#     #     cleaned_title = re.sub(r"\b(?:latest|new)?\s*\w+(?:\s+\w+)?\s+songs?\s*\{?\d{4}\}?","",cleaned_title,flags=re.IGNORECASE).strip()
        
#     #     # Remove years and associated separators (e.g., "- 2023" or "/2022")
#     #     cleaned_title = re.sub(
#     #         r'(\s*[-/]?\s*\b(19|20)\d{2}\b)', 
#     #         '', 
#     #         cleaned_title
#     #     )

#     #     # Step 2: Remove characters NOT in Hindi (Unicode), Punjabi (Gurmukhi), English, digits, or common QWERTY symbols
#     #     cleaned_title = re.sub(
#     #         r"[^\u0900-\u097F\u0A00-\u0A7F\w\s\-\.,!@#$%^&*()_+=|\\{}\[\]:;\"'<>\?/`~]", 
#     #         "", 
#     #         cleaned_title
#     #     )

#     #     # Step 3: Trim leading/trailing non-word characters (symbols or spaces)
#     #     cleaned_title = re.sub(r"^[^\w\u0900-\u097F\u0A00-\u0A7F]+|[^\w\u0900-\u097F\u0A00-\u0A7F]+$", "", cleaned_title)

        
#     #     # Remove anything after last pipe character
#     #     # if '|' in cleaned_title:
#     #     #     cleaned_title = cleaned_title.rsplit('|', 1)[0]
            
#     #     # Clean up residual characters and whitespace
#     #     # cleaned_title = re.sub(r'[^\w\s-]', '', cleaned_title)  # Remove special chars
#     #     cleaned_title = re.sub(r'\s+', ' ', cleaned_title)      # Collapse whitespace
#     #     return cleaned_title.strip()

# class SongPool:
#     def __init__(self):
#         self._songs = {}
#         self._lock = threading.Lock()

#     def add_song(self, song: Song) -> bool:
#         with self._lock:
#             if song.video_id not in self._songs:
#                 self._songs[song.video_id] = song
#                 return True
#             return False

#     def get_song(self, video_id: str) -> Optional[Song]:
#         with self._lock:
#             return self._songs.get(video_id)

#     def get_songs_by_ids(self, video_ids: List[str]) -> List[Song]:
#         with self._lock:
#             return [self._songs[vid] for vid in video_ids if vid in self._songs]

#     def get_all_songs(self) -> List[Song]:
#         with self._lock:
#             return list(self._songs.values())

import threading
from typing import Optional, List
import re
from utils.telegram_logger import telegram_handler
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.addHandler(telegram_handler)
logger.setLevel(logging.INFO)


_PHRASES = [
    # Official content variants
    r"official\s+(video|song|audio|lyrics?)",  
    r"official\s+.*?song\b",
    
    # Feature/production tags
    r"\b(ft\.?|feat\.?|prod\.?|remix|version|mix|dj)\b.*",
    
    # Quality/format tags
    r"\b(hd|4k|mp3|viral|lyrical|dance performance|3d audio|non stop|full video|video song|song promo)\b",
    
    # Regional song patterns
    r"\b(new|latest|best)\s+(haryanvi|punjabi|rajasthani)(\s*&\s*(haryanvi|punjabi|rajasthani))?\s+songs?\b",
    
    # Platform references and years
    r"\bvyrl\b",
    r"\b\d{4}\b",
    
    # DJ variations
    r"\b(d\s?j\.?|dj)\s*song\b",
    
    # Common redundant phrases
    r"\boriginal\s+song\b",
    r"\bnon\s+stop\s+(haryanvi|punjabi|rajasthani)\b",
    r"\bdance\s+video\b",
    r"\bfull\s+video\s+with\s+lyrics\b",
    r"\bbest\s+song\b",
    r"\b(new|latest)\s+haryanvi\s*&\s*rajasthani\s+song\b",
]

_REMOVAL_PATTERNS = {
    "phrases": re.compile(
        "(?:" + "|".join(_PHRASES) + ")",
        flags=re.IGNORECASE | re.UNICODE
    ),
    "metadata": re.compile(
        r"""
        [\[\(].*?[\]\)]|      # Brackets/parentheses content
        [@#&]\w+|               # Leading @, #, & words
        \w+[@#&]|               # Trailing @, #, & words
        -\s*\d{4}$|            # Trailing year with hyphen
        \s*[|•.]\s*.*          # Content after separators
        """, 
        flags=re.IGNORECASE | re.UNICODE | re.VERBOSE
    ),
    "cleanup": re.compile(
        r"[^\w\u0900-\u097F\u0A00-\u0A7F\s.,!&+'?-]",
        flags=re.UNICODE
    )
}

_TRIM_PATTERN = re.compile(
    r"^\W+|\W+$",  # Trim leading/trailing non-word chars
    flags=re.UNICODE
)

class TitleCleaner:
    @staticmethod
    def clean_title(raw_title: str) -> str:
        
        """Optimized multilingual title cleaner"""
        if not raw_title:
            return ""
        # logger.warning("Previous : "+raw_title)
        # Phase 1: Remove large chunks
        title = _REMOVAL_PATTERNS["phrases"].sub('', raw_title)
        # Phase 2: Remove metadata, mentions, hashtags, attached symbol words
        title = _REMOVAL_PATTERNS["metadata"].sub('', title)
        # Phase 3: Cleanup remaining unwanted characters
        title = _REMOVAL_PATTERNS["cleanup"].sub('', title)
        # Final processing: trim edges and collapse spaces
        title = _TRIM_PATTERN.sub('', title)
        title = re.sub(r'\s+', ' ', title).strip()

        # Fallback to first 50 chars of raw if nothing remains
        # logger.warning("After Clean : "+title or raw_title[:50])
        logger.warning(f"Clean title – before: “{raw_title}”, after: “{title}”")
        return title or raw_title[:50]

class Song:
    def __init__(self, video_id: str, title: str, thumbnail: str, duration: int = 0):
        if not video_id or not title or not thumbnail:
            raise ValueError("video_id, title, and thumbnail are required")
        self.video_id = video_id
        self.title = TitleCleaner.clean_title(title)
        self.thumbnail = thumbnail
        self.duration = duration
        self.play_count = 0
        self.audio_url: Optional[str] = None

    @classmethod
    def from_video_id(cls, video_id: str):
        """Alternative constructor that fetches metadata from audio service"""
        import audioV3  # Import inside method to avoid circular imports
        
        # Fetch song details from external service
        details = audioV3. get_video_info(video_id)
        if not details:
            raise ValueError(f"Could not fetch details for video ID: {video_id}")
            
        return cls(
            video_id=video_id,
            title=details['title'],
            thumbnail=details['thumbnail'],
            duration=details.get('duration', 0)
        )

    def is_valid(self) -> bool:
        excluded = {"lofi", "slowed", "reverb", "nightcore"}
        t = self.title.lower()
        return 90 <= self.duration <= 1200 and not any(k in t for k in excluded)

    def increment_play_count(self) -> None:
        self.play_count += 1

    def update_audio_url(self, url: str) -> None:
        self.audio_url = url

    def to_dict(self) -> dict:
        return {
            "videoId": self.video_id,
            "title": self.title,
            "thumbnail": self.thumbnail,
            "duration": self.duration,
            "playCount": self.play_count,
            "audioUrl": self.audio_url,
        }

class SongPool:
    def __init__(self):
        self._songs: dict[str, Song] = {}
        self._lock = threading.Lock()

    def add_song(self, song: Song) -> bool:
        with self._lock:
            if song.video_id not in self._songs:
                self._songs[song.video_id] = song
                return True
            return False

    def get_song(self, video_id: str) -> Optional[Song]:
        with self._lock:
            return self._songs.get(video_id)

    def get_songs_by_ids(self, ids: List[str]) -> List[Song]:
        with self._lock:
            return [self._songs[i] for i in ids if i in self._songs]

    def get_all_songs(self) -> List[Song]:
        with self._lock:
            return list(self._songs.values())
