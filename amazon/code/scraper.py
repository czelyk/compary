import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from utils import is_amazon_link

def scrape_amazon_product(url):
    """Scrape product details & comments using Selenium."""
    if not is_amazon_link(url):
        print("Error: The provided URL is not a valid Amazon link.")
        return

    # Set up results directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")  # Reduce console logs

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2)  # Wait for page to load

        # Extract product title
        try:
            product_name = driver.find_element(By.ID, "productTitle").text.strip()
        except:
            product_name = "Unknown Product"

        # Extract star rating
        try:
            star_element = driver.find_element(By.XPATH, "//span[contains(@class, 'a-icon-alt')]")
            star_rating = star_element.text.split(" ")[-1]  # Extract last number (e.g., "4.7")
        except:
            star_rating = "N/A"

        # Scroll down to load reviews
        try:
            reviews_section = driver.find_element(By.ID, "reviewsMedley")
            driver.execute_script("arguments[0].scrollIntoView();", reviews_section)
            time.sleep(2)  # Wait for reviews to load
        except:
            print("Reviews section not found, skipping scroll.")

        # Extract all comments
        comments = []
        review_elements = driver.find_elements(By.XPATH, "//div[@data-hook='review-collapsed']//span")

        for idx, review in enumerate(review_elements, start=1):
            comment_text = review.text.strip()
            if comment_text:
                comments.append(f"Comment #{idx}: {comment_text}")

        # Save results to file
        if product_name:
            words = product_name.split()
            filename = "_".join(words[:2]) + ".txt"
            file_path = os.path.join(RESULTS_DIR, filename)

            formatted_text = f"Product Name: {product_name}\nStars: {star_rating}\n\n"
            if comments:
                formatted_text += "\n".join(comments)
            else:
                formatted_text += "No comments found."

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(formatted_text)

            print(f"✅ Product details and comments saved successfully: {file_path}")

        else:
            print("Error: Could not find the product title.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()  # Close the browser

