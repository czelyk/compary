import requests
from bs4 import BeautifulSoup
import re
import os
import sys
from fake_useragent import UserAgent

def is_amazon_link(url):
    """Check if the URL is a valid Amazon link."""
    pattern = r"https?://(?:www\.)?amazon\.(com|co\.[a-z]{2,3}|ca|co\.uk|de|fr|it|es|in|jp|mx|com\.br|com\.au|co\.jp|cn|com\.tr)/"
    return bool(re.match(pattern, url))

def scrape_amazon_product(url):
    """Scrape the product title and save it to a file."""
    if not is_amazon_link(url):
        print("Invalid Amazon link.")
        return

    # Define directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Get a random user-agent
    ua = UserAgent()
    headers = {"User-Agent": ua.random}  # Automatically choose a random user-agent

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for failed requests
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    product_name = soup.find("span", id="productTitle")

    if product_name:
        product_text = product_name.get_text(strip=True)

        # Extract first two words for filename
        words = re.findall(r'\w+', product_text)
        filename = "_".join(words[:2]) + ".txt"

        file_path = os.path.join(RESULTS_DIR, filename)

        formatted_text = f"Product name: {product_text}"

        # Save to file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(formatted_text)

        print(f"Product name saved to {file_path}")
    else:
        print("Product title not found. Amazon may have blocked the request.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scrape_amazon_product(sys.argv[1])  # Get URL from command-line argument
    else:
        print("Usage: python scraping.py <Amazon URL>")
