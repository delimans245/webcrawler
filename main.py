import sys
import asyncio
from crawl import crawl_site_async

async def main_async():
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <url> [max_concurrency] [max_pages]")
        print("Example: python main.py https://example.com 5 100")
        sys.exit(1)
        
    base_url = sys.argv[1]
    
    # Default values
    max_concurrency = 5
    max_pages = 100
    
    # Parse optional arguments
    if len(sys.argv) >= 3:
        try:
            max_concurrency = int(sys.argv[2])
        except ValueError:
            print("max_concurrency must be an integer")
            sys.exit(1)
    
    if len(sys.argv) >= 4:
        try:
            max_pages = int(sys.argv[3])
        except ValueError:
            print("max_pages must be an integer")
            sys.exit(1)

    print(f"Starting async crawl of: {base_url}")
    print(f"Max concurrency: {max_concurrency}")
    print(f"Max pages: {max_pages}\n")

    pages = await crawl_site_async(base_url, max_concurrency, max_pages)

    # Print the formatted report
    from crawl import print_report
    print_report(pages, base_url)

if __name__ == "__main__":
    asyncio.run(main_async())