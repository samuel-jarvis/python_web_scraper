import requests
from bs4 import BeautifulSoup
import sys
from pprint import pprint
import json

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.example.com"
books2Scrape = "http://books.toscrape.com"


def get_html(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print('there was an error getting the page:', e)
        sys.exit(1)


def parse_html(html):
    html = get_html(books2Scrape)
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("title")
    title = title_tag.text if title_tag else None

    print(title)

    books = soup.select(".product_pod")

    data = []

    for book in books:
        a_tag = book.select_one("h3 a")
        a_text = a_tag.get_text(strip=True)

        item = {
            "name": a_text,
            "price": book.select_one('.price_color').text
        }

        data.append(item)

    pprint(data)
    return data


html = get_html(books2Scrape)
books = parse_html(html)

with open('books.json', 'w') as f:
    json.dump(books, f, indent=4)


# Get book and their details
response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, "html.parser")
# get links for the books pages
book_links = soup.select_one('.product_pod .image_container a')
Console.log(book_links)
