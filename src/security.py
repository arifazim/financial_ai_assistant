# AI safety and compliance checks 
##### src/security.py #####
def validate_response(response: str):
    if any(unsafe_word in response.lower() for unsafe_word in ["malware", "phishing"]):
        return "[REDACTED: Unsafe Content]"
    return response