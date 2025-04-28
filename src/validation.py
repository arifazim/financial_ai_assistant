# Accuracy and safety checks 
import re

def validate_query(query: str) -> bool:
    """
    Validates user queries to prevent harmful input.
    Returns True if safe, False if rejected.
    """
    blacklist = ["DROP TABLE", "DELETE FROM", "--", ";--", "xp_cmdshell"]
    
    if any(term in query.upper() for term in blacklist):
        return False
    
    if len(query) > 500:
        return False  # Prevent overly long queries
    
    return True

def sanitize_input(text: str) -> str:
    """
    Cleans input by removing special characters and extra spaces.
    """
    return re.sub(r"[^a-zA-Z0-9\s.,!?]", "", text).strip()
