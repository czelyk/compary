import os
import re
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import ollama
from utils import is_amazon_link

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Set up results directory inside `amazon/`
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
COMMENTS_DIR = os.path.join(RESULTS_DIR, "Comments")
AI_SUMMARY_DIR = os.path.join(RESULTS_DIR, "AI Summary")

os.makedirs(COMMENTS_DIR, exist_ok=True)
os.makedirs(AI_SUMMARY_DIR, exist_ok=True)

def scrape_amazon_product(url):
    """
    Scrapes Amazon product details and comments, then summarizes using AI.
    Saves comments and AI summary in the `results` directory.
    """
    if not is_amazon_link(url):
        logging.error("❌ Error: The provided URL is not a valid Amazon link.")
        return

    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)

        # Extract product title
        try:
            product_name = driver.find_element(By.ID, "productTitle").text.strip()
        except:
            product_name = "Unknown Product"

        # Extract star rating
        try:
            star_element = driver.find_element(By.XPATH, "//span[contains(@class, 'a-icon-alt')]")
            star_rating = star_element.text.split(" ")[-1]
        except:
            star_rating = "N/A"

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
            file_path = os.path.join(COMMENTS_DIR, filename)
            summary_path = os.path.join(AI_SUMMARY_DIR, filename)

            formatted_text = f"Product Name: {product_name}\nStars: {star_rating}\n\n"
            if comments:
                formatted_text += "\n".join(comments)
            else:
                formatted_text += "No comments found."

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(formatted_text)

            logging.info(f"✅ Comments saved successfully: {file_path}")

            # 🎯 Send to AI and save summary
            summarize_text_with_ai(file_path, summary_path)

        else:
            logging.error("❌ Error: Could not find the product title.")

    except Exception as e:
        logging.error(f"❌ Error: {e}")

    finally:
        driver.quit()

def summarize_text_with_ai(input_file, output_file):
    """
    Reads scraped text, summarizes using AI, and saves the result.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            text_content = file.read()

        # 🧠 Send text to AI
        response = ollama.chat(
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "Summarize the key points from the comments."},
                {"role": "user", "content": text_content}
            ]
        )

        ai_summary = response["message"]["content"]

        # 🧹 Clean AI response
        ai_summary_cleaned = re.sub(r"<think>.*?</think>", "", ai_summary, flags=re.DOTALL).strip()

        # Save AI-generated summary
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(ai_summary_cleaned)

        logging.info(f"✅ AI summary saved successfully: {output_file}")

    except Exception as e:
        logging.error(f"❌ Error: Failed to summarize text. {e}")
