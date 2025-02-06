import re

def sanitize_url(url):
    sanitized_url = re.sub(r'[^a-zA-Z0-9:/?&=._-]', '', url)
    return sanitized_url
