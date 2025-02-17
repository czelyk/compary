import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
from utils import is_amazon_link

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

    # Extract the product title from the meta tag
    meta_title = soup.find("meta", attrs={"name": "title"})
    if meta_title:
        product_name = meta_title.get("content")
    else:
        product_name = None

    if product_name:
        # Extract first two words for filename
        words = product_name.split()
        filename = "_".join(words[:2]) + ".txt"

        file_path = os.path.join(RESULTS_DIR, filename)

        formatted_text = f"Product name: {product_name}"

        # Save to file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(formatted_text)

        print(f"✅ Product name saved successfully: {file_path}")
    else:
        print("Error: Could not find the product title. Amazon may have blocked the request or changed its structure.")
