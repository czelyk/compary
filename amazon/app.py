import re



def is_amazon_link(url):
    # Regular expression pattern to match Amazon URLs, including Amazon Turkey
    pattern = r"https?://(?:www\.)?amazon\.(com|co\.[a-z]{2,3}|ca|co\.uk|de|fr|it|es|in|jp|mx|com\.br|com\.au|co\.jp|cn|com\.tr)/"
    if re.match(pattern, url):
        return True
    return False

def main():
    # Get URL from user input
    url = input("Enter the URL: ")

    if is_amazon_link(url):
        print(f"The URL is an Amazon link.")
    else:
        print(f"The URL is NOT an Amazon link.")

if __name__ == "__main__":
    main()

