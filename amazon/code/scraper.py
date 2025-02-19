import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import ollama
from utils import is_amazon_link

def scrape_amazon_product(url):
    """Scrape Amazon product details & comments, then summarize using AI."""
    if not is_amazon_link(url):
        print("Error: The provided URL is not a valid Amazon link.")
        return

    # Set up results directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")
    COMMENTS_DIR = os.path.join(RESULTS_DIR, "Comments")
    AI_SUMMARY_DIR = os.path.join(RESULTS_DIR, "AI Summary")

    os.makedirs(COMMENTS_DIR, exist_ok=True)
    os.makedirs(AI_SUMMARY_DIR, exist_ok=True)

    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")  # Reduce console logs

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
            star_rating = star_element.text.split(" ")[-1]  # Extract last number (e.g., "4.7")
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
            filename = "_".join(words[:2]) + ".txt"  # e.g., "Apple_iPhone.txt"
            file_path = os.path.join(COMMENTS_DIR, filename)
            summary_path = os.path.join(AI_SUMMARY_DIR, filename)

            formatted_text = f"Product Name: {product_name}\nStars: {star_rating}\n\n"
            if comments:
                formatted_text += "\n".join(comments)
            else:
                formatted_text += "No comments found."

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(formatted_text)

            print(f"✅ Comments saved successfully: {file_path}")

            # 🎯 Send to AI and save summary
            summarize_text_with_ai(file_path, summary_path)

        else:
            print("Error: Could not find the product title.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()  # Close the browser

def summarize_text_with_ai(input_file, output_file):
    """Read the scraped text file, send to AI for summarization, clean unnecessary text, and save result."""
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            text_content = file.read()

        # 🧠 Send text to AI (DeepSeek)
        response = ollama.chat(
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "Summarize the key points from the comments."},
                {"role": "user", "content": text_content}
            ]
        )

        ai_summary = response["message"]["content"]

        # 🧹 Remove any "<think>...</think>" sections
        ai_summary_cleaned = re.sub(r"<think>.*?</think>", "", ai_summary, flags=re.DOTALL).strip()

        # Save AI-generated summary
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(ai_summary_cleaned)

        print(f"✅ AI summary saved successfully: {output_file}")

    except Exception as e:
        print(f"Error: Failed to summarize text. {e}")