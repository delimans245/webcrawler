import asyncio
import aiohttp
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
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower().rstrip('/')
    return f"{host}{path}" if path else host
    

async def get_urls_from_html(html, base_url):
    """
    Reads a page of HTML text and extract links
    """
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href or not href.strip():
            continue
            
        try:
            if href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                continue
                
            absolute_url = urljoin(base_url, href)
            parsed = urlparse(absolute_url)
            
            if not parsed.netloc or parsed.scheme not in ('http', 'https', ''):
                continue
                
            urls.append(absolute_url)
        except ValueError:
            continue
            
    return urls

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=5, max_pages=100):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.pages = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if len(self.pages) >= self.max_pages:
                return False
                
            if normalized_url in self.pages:
                self.pages[normalized_url] += 1
                return False
                
            self.pages[normalized_url] = 1
            return True

    async def get_html(self, url):
        try:
            async with self.semaphore:
                async with self.session.get(url) as response:
                    if response.status != 200:
                        raise ValueError(f"HTTP status {response.status}")
                    
                    content_type = response.headers.get('content-type', '')
                    if 'text/html' not in content_type:
                        raise ValueError(f"URL did not return HTML (content-type: {content_type})")
                    
                    return await response.text()
        except Exception as e:
            raise ValueError(f"Failed to fetch {url}: {str(e)}")

    async def crawl_page(self, current_url):
        # Check if we've reached max pages
        async with self.lock:
            if len(self.pages) >= self.max_pages:
                return

        current_domain = urlparse(current_url).netloc
        if current_domain != self.base_domain:
            return

        normalized_url = normalize_url(current_url)
        
        if not await self.add_page_visit(normalized_url):
            return

        print(f"Crawling: {current_url}")

        try:
            html = await self.get_html(current_url)
            urls = await get_urls_from_html(html, current_url)
            
            tasks = [asyncio.create_task(self.crawl_page(url)) for url in urls]
            await asyncio.gather(*tasks)
            
        except Exception as e:
            print(f"Error crawling {current_url}: {str(e)}")

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.pages

async def crawl_site_async(base_url, max_concurrency=5, max_pages=100):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()

def print_report(pages, base_url):
    """
    Prints a formatted report of the crawl results
    
    Args:
        pages (dict): Dictionary of pages and their counts
        base_url (str): The base URL that was crawled
    """
    # Print report header
    print("\n" + "="*30)
    print(f"  REPORT for {base_url}")
    print("="*30 + "\n")
    
    # Sort pages by count (descending) and then by URL (ascending)
    sorted_pages = sorted(
        pages.items(),
        key=lambda item: (-item[1], item[0])
    )  # Negative count for descending
    
    # Print each page entry
    for url, count in sorted_pages:
        print(f"Found {count} internal links to {url}")
    
    # Print summary
    print(f"\nTotal pages crawled: {len(pages)}")