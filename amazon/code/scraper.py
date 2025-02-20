import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils import is_amazon_link
from ai_processing import summarize_text_with_ai
from config import COMMENTS_DIR, AI_SUMMARY_DIR


def scrape_amazon_product(url: str):
    """Scrape Amazon product details & comments, then summarize using AI."""
    if not is_amazon_link(url):
        print("❌ Error: The provided URL is not a valid Amazon link.")
        return

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)

        # Extract product title
        product_name = driver.find_element(By.ID, "productTitle").text.strip() if driver.find_elements(By.ID,
                                                                                                       "productTitle") else "Unknown Product"

        # Extract star rating
        star_rating = driver.find_element(By.XPATH, "//span[contains(@class, 'a-icon-alt')]").text.split(" ")[
            -1] if driver.find_elements(By.XPATH, "//span[contains(@class, 'a-icon-alt')]") else "N/A"

        # Extract comments
        comments = [review.text.strip() for review in
                    driver.find_elements(By.XPATH, "//div[@data-hook='review-collapsed']//span") if review.text.strip()]

        if not comments:
            comments = ["No comments found."]

        # Save results
        filename = "_".join(product_name.split()[:2]) + ".txt"
        file_path = os.path.join(COMMENTS_DIR, filename)
        summary_path = os.path.join(AI_SUMMARY_DIR, filename)

        formatted_text = f"Product Name: {product_name}\nStars: {star_rating}\n\n" + "\n".join(comments)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(formatted_text)

        print(f"✅ Comments saved successfully: {file_path}")

        # Summarize with AI
        summarize_text_with_ai(file_path, summary_path)

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()
