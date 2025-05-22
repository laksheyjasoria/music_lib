from typing import Union

def is_valid_song(title: str, duration: Union[int, float]) -> bool:
    """
    Validate if a song meets our criteria
    - Duration between 90 and 1200 seconds (1.5-20 minutes)
    - Doesn't contain excluded terms in title
    """
    excluded_terms = {
        "lofi", "slowed", "reverb", "nightcore",
        "remix", "dj remix", "djremix", "d.j remix",
        "d.j. remix", "dj mix", "djmix", "d.j mix"
    }
    
    if not 90 <= duration <= 1200:
        return False
        
    lower_title = title.lower()
    return not any(term in lower_title for term in excluded_terms)
