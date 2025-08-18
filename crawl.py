from urllib.parse import urlparse

def normalize_url(url):
    """
    Normalizes a URL by:
    - Removing protocol (http/https)
    - Converting to lowercase
    - Removing trailing slashes
    - Removing query parameters and fragments
    
    Args:
        url (str): The URL to normalize
        
    Returns:
        str: The normalized URL (e.g. "blog.boot.dev/path")
    """
    # Parse the URL
    parsed = urlparse(url)
    
    # Combine netloc (domain) and path
    host = parsed.netloc.lower()
    path = parsed.path.lower().rstrip('/')
    
    # Construct normalized URL
    normalized = f"{host}{path}" if path else host

    return normalized
    

def get_urls_from_html(html, base_url):
    pass