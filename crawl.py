from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

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
    
    #create BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    #result that we will return
    urls = []
    
    #placeholder for all a tags
    all_a_tags = soup.find_all('a')

    #traverse through all a tags that we have found
    for link in all_a_tags:
        href = link.get('href')
        if not href or not href.strip():  # Skip empty or whitespace-only hrefs
            continue
            
        try:
            # Skip non-HTTP links and invalid formats
            if href.startswith(('mailto:', 'tel:', 'javascript:', '#')) or href == 'invalid-url':
                continue
                
            # Handle relative URLs
            absolute_url = urljoin(base_url, href)
            parsed = urlparse(absolute_url)
            
            # Only keep URLs with network location and valid scheme
            if not parsed.netloc or parsed.scheme not in ('http', 'https', ''):
                continue
                
            urls.append(absolute_url)
        except ValueError:
            continue
            
    return urls