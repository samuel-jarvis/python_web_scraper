from urllib.parse import urljoin
from bs4 import BeautifulSoup
from scraper.models.book import BookCreate


def parse_book_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for tag in soup.select('.product_pod .image_container a'):
        href = tag.get("href")
        if href:
            links.append(urljoin(base_url, href))
    return links


def parse_product_table(soup: BeautifulSoup) -> dict[str, str]:
    info: dict[str, str] = {}
    for row in soup.select("table.table-striped tr"):
        th = row.find("th")
        td = row.find("td")
        if th and td:
            info[th.get_text(strip=True)] = td.get_text(strip=True)
    return info


def parse_book_detail(html: str, book_url: str) -> BookCreate:
    soup = BeautifulSoup(html, "html.parser")

    name_tag = soup.select_one(".product_main h1")
    price_tag = soup.select_one(".product_main .price_color")
    desc_tag = soup.select_one("#product_description ~ p")

    name = name_tag.get_text(strip=True) if name_tag else None
    price = price_tag.get_text(strip=True) if price_tag else None
    description = desc_tag.get_text(strip=True) if desc_tag else None

    information = parse_product_table(soup)

    return BookCreate(
        name=name,
        book_url=book_url,
        price=price,
        description=description,
        information=information
    )
