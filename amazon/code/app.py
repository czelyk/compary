import re
import subprocess

def is_amazon_link(url):
    """Check if the URL is a valid Amazon link."""
    pattern = r"https?://(?:www\.)?amazon\.(com|co\.[a-z]{2,3}|ca|co\.uk|de|fr|it|es|in|jp|mx|com\.br|com\.au|co\.jp|cn|com\.tr)/"
    return bool(re.match(pattern, url))

def main():
    url = input("Enter the Amazon URL: ").strip()

    if is_amazon_link(url):
        print("Valid Amazon URL. Scraping data...")
        subprocess.run(["python", "scraping.py", url])  # Call scraping.py with URL
    else:
        print("Invalid Amazon link. Please enter a valid Amazon product URL.")

if __name__ == "__main__":
    main()
