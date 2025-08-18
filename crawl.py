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
    """
    Reads a page of HTML text and extract links

    Args:
        html (str): The html file that we look through
        base_url (str) : Root URL of the website we are crawling

    Returns:
        Array of strings of un-normalized list of all the URLs found within the HTML, and an error if one occurs.
    """
    pass