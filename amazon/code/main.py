from scraper import scrape_amazon_product

def main():
    url = input("Enter the Amazon product URL: ").strip()
    if url:
        scrape_amazon_product(url)
    else:
        print("❌ Please provide a valid Amazon URL.")

if __name__ == "__main__":
    main()
