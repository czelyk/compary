import re

def is_amazon_link(url: str) -> bool:
    """Check if the URL is a valid Amazon link."""
    pattern = r"https?://(?:www\.)?amazon\.(com|co\.[a-z]{2,3}|ca|co\.uk|de|fr|it|es|in|jp|mx|com\.br|com\.au|co\.jp|cn|com\.tr)/"
    return bool(re.match(pattern, url))
