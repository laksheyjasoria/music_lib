# import re
# import spacy

# # Load spaCy’s small English model
# nlp = spacy.load("en_core_web_sm")

# def extract_song_name(title: str) -> str:
#     """
#     Given a YouTube-style title, return just the song name as a string
#     """
#     doc = nlp(title)
    
#     # First try to extract WORK_OF_ART entity
#     songs = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
#     if songs:
#         return songs[0]
    
#     # Fallback regex pattern (now includes colon as a separator)
#     m = re.match(r"^(.*?)(?=\s*[|\(–—:])", title)
#     return m.group(1).strip() if m else title.strip()

# if __name__ == "__main__":
#     # Test with sample titles
#     examples = [...]  # Your example array here
#     for t in examples:
#         print(f"Title: {t}\n → Song: {extract_song_name(t)}\n")


import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_song_name(title: str) -> str:
    """
    Improved version that handles various title formats commonly found in Haryanvi songs
    """
    # Clean title first
    title = re.sub(r'\s+', ' ', title).strip()  # Normalize whitespace
    
    # Try spaCy's WORK_OF_ART detection first
    doc = nlp(title)
    songs = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
    if songs:
        return songs[0]
    
    # Enhanced regex pattern with multiple fallbacks
    patterns = [
        r"^(.*?)(?:\s*[|\(\-–—:・•]| ft\.| feat\.| by| with)",  # Common separators
        r"^([^\]】]+)(?:[\]】])",  # Text inside brackets
        r"^(.*?)\s*(?:official|video|lyrical|audio|song|hd|haryanvi|202\d)",  # Common suffixes
        r"^(.*?)\s*(?:full video|visualizer|remake|remix|mix|version)", 
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, flags=re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            if len(candidate) >= 4:  # Minimum reasonable song name length
                return candidate
    
    # Final fallback: Split on first special character cluster
    final_match = re.match(r"^([\w\s]+(?=\s*[^\w\s]))", title)
    return final_match.group(1).strip() if final_match else title.strip()

if __name__ == "__main__":
    examples = [...]  # Your example array here
    for t in examples:
        print(f"Title: {t}\n → Song: {extract_song_name(t)}\n")
