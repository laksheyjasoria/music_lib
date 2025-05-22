import re
from typing import List

_PHRASES = [
    r"official\s+(video|song|audio|lyrics?)",  
    r"official\s+.*?song\b",
    r"\b(ft\.?|feat\.?|prod\.?|remix|version|mix|dj)\b.*",
    r"\b(hd|4k|mp3|viral|lyrical|dance performance|3d audio|non stop|full video)\b",
    r"\b(new|latest|best)\s+(haryanvi|punjabi|rajasthani)(\s*&\s*(haryanvi|punjabi|rajasthani))?\s+songs?\b",
    r"\bvyrl\b",
    r"\b\d{4}\b",
    r"\b(d\s?j\.?|dj)\s*song\b",
    r"\boriginal\s+song\b",
    r"\bnon\s+stop\s+(haryanvi|punjabi|rajasthani)\b",
    r"\bdance\s+video\b",
    r"\bfull\s+video\s+with\s+lyrics\b",
    r"\bbest\s+song\b",
]

class TitleCleaner:
    _removal_patterns = {
        "phrases": re.compile("|".join(_PHRASES), flags=re.IGNORECASE),
        "metadata": re.compile(
            r"[\[\(].*?[\]\)]|[#@&]\w+|\w+[#@&]|-\s*\d{4}$|\s*[|•.]\s*.*",
            flags=re.IGNORECASE
        ),
        "cleanup": re.compile(r"[^\w\u0900-\u097F\u0A00-\u0A7F\s.,!&+'?-]", flags=re.UNICODE),
        "trim": re.compile(r"^\W+|\W+$")
    }

    @classmethod
    def clean_title(cls, raw_title: str) -> str:
        if not raw_title:
            return ""
            
        title = cls._removal_patterns["phrases"].sub('', raw_title)
        title = cls._removal_patterns["metadata"].sub('', title)
        title = cls._removal_patterns["cleanup"].sub('', title)
        title = cls._removal_patterns["trim"].sub('', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title or raw_title[:50]
