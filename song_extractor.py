import re
import spacy

# Load spaCy’s small English model
nlp = spacy.load("en_core_web_sm")

def extract_song_name(title: str) -> str:
    """
    Given a YouTube-style title, return just the song name as a string
    """
    doc = nlp(title)
    
    # First try to extract WORK_OF_ART entity
    songs = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
    if songs:
        return songs[0]
    
    # Fallback regex pattern (now includes colon as a separator)
    m = re.match(r"^(.*?)(?=\s*[|\(–—:])", title)
    return m.group(1).strip() if m else title.strip()

if __name__ == "__main__":
    # Test with sample titles
    examples = [...]  # Your example array here
    for t in examples:
        print(f"Title: {t}\n → Song: {extract_song_name(t)}\n")
