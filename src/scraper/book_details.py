import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scraper.repository.book_repository import BookRepository
from scraper.models.book import BookCreate
from scraper.logger import logger

books2Scrape = "http://books.toscrape.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}
# Get book and their details

try:
    response = requests.get(books2Scrape, headers=headers, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    logger.error('There was an error getting the page: %s', e)
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")

# get links for the books pages
book_links = soup.select('.product_pod .image_container a')
logger.debug('Found %d book links', len(book_links))

links = [tag['href'] for tag in book_links if tag.has_attr('href')]
logger.debug('Found %d hrefs', len(links))

data = []

book_repo = BookRepository()

for book in links:
    book_url = urljoin(books2Scrape, book)
    logger.info('Processing book URL: %s', book_url)

    # get the book page and parse it
    book_response = requests.get(book_url, headers=headers, timeout=10)
    book_response.raise_for_status()
    book_response.encoding = book_response.apparent_encoding
    book_page_soup = BeautifulSoup(book_response.text, "html.parser")

    # extract book details
    book_name_tag = book_page_soup.select_one(".product_main h1")
    logger.debug('book_name_tag: %s', book_name_tag)
    book_name = book_name_tag.get_text(strip=True) if book_name_tag else None

    # extract price
    book_price_tag = book_page_soup.select_one(".product_main .price_color")
    book_price = book_price_tag.get_text(
        strip=True) if book_price_tag else None

    # extract description
    book_description_tag = book_page_soup.select_one(".product_page > p")
    book_description = book_description_tag.get_text(
        strip=True) if book_description_tag else None

    # get book table details
    product_data = {}
    table_rows = book_page_soup.select('table.table-striped tr')

    for row in table_rows:
        th = row.find('th')
        td = row.find('td')

        if th and td:
            key = th.text.strip()
            value = td.text.strip()
            product_data[key] = value

    item = {
        "name": book_name,
        "book_url": book_url,
        "price": book_price,
        "description": book_description,
        "information": product_data
    }

    data.append(item)
    logger.debug('Appended book item: %s', item)

    book_repo.create_book(BookCreate(**item))

with open('books-description.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

logger.info('Saved %d book descriptions to books-description.json', len(data))
