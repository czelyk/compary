from scraper import scrape_amazon_product

def main():
    url = input("Enter the Amazon product URL: ").strip()  # Take URL input from the user
    if url:
        scrape_amazon_product(url)  # Scrape the product with the provided URL
    else:
        print("Please provide a valid Amazon URL.")

if __name__ == "__main__":
    main()
