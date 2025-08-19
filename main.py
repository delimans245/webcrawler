import sys
from crawl import get_html, crawl_page
def main():
    if (len(sys.argv) < 2):
        print("no website provided")
        sys.exit(1)
    elif (len(sys.argv) > 2):
        print("too many arguments")
        sys.exit(1)
    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")
    pages = crawl_page(base_url)

    print("\nFound pages:")
    for url, count in pages.items():
        print(f"{url}: {count}")




if __name__ == "__main__":
    main()

