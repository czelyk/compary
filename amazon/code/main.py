import sys
from scraper import scrape_amazon_product

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        scrape_amazon_product(url)  # Scrape the product with the provided URL
    else:
        print("Usage: python main.py <Amazon URL>")

if __name__ == "__main__":
    main()
