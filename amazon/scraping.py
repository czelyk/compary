import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.com.tr/Geometrik-Rafl%C4%B1-A%C4%9Fa%C3%A7-Kitapl%C4%B1k-Dekorasyonu/dp/B0DRYH2TCT"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
}

session = requests.Session()
response = session.get(URL, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    product_name = soup.find("span", id="productTitle")

    if product_name:
        print(product_name.get_text(strip=True))
    else:
        print("Product title not found. Amazon may have blocked the request.")
else:
    print(f"Failed to fetch page, status code: {response.status_code}")
