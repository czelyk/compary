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
        print("Error: The provided URL is not a valid Amazon link.")
        return

    # Define directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Get a random user-agent
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for failed requests
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Amazon may be blocking the request.")
        return
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
        return
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to Amazon. Please check your internet connection.")
        return
    except requests.exceptions.RequestException as err:
        print(f"Error: An unexpected request error occurred: {err}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Try multiple ways to find the product title
    product_name = soup.find("span", id="productTitle")
    if not product_name:
        product_name = soup.find("h1", class_="a-size-large a-spacing-none")  # Alternative selector

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

        print(f"✅ Product name saved successfully: {file_path}")
    else:
        print("Error: Could not find the product title. Amazon may have blocked the request or changed its structure.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scrape_amazon_product(sys.argv[1])  # Get URL from command-line argument
    else:
        print("Usage: python scraping.py <Amazon URL>")
