"""
Book Scraper
Scrapes book data (title, price, rating, availability, URL) from the demo
website https://books.toscrape.com and saves it as CSV and Excel.

Usage:
    python scraper.py
"""

import re
import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
OUTPUT_DIR = Path("output")
DELAY_SECONDS = 0.5  # be polite to the server
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; BookScraper/1.0)"}

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch(url, session, retries=3):
    """Download a page with simple retry logic."""
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            response.encoding = "utf-8"  # avoids broken £ symbol
            return response.text
        except requests.RequestException as error:
            print(f"  Attempt {attempt}/{retries} failed for {url}: {error}")
            time.sleep(2)
    raise RuntimeError(f"Could not fetch {url} after {retries} attempts")


def parse_page(html, page_url):
    """Extract all books from one listing page and the next page URL."""
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for item in soup.select("article.product_pod"):
        link = item.select_one("h3 a")
        price_text = item.select_one("p.price_color").get_text(strip=True)
        rating_word = item.select_one("p.star-rating")["class"][1]
        availability = item.select_one("p.availability").get_text(strip=True)

        books.append(
            {
                "title": link["title"],
                "price_gbp": float(re.sub(r"[^\d.]", "", price_text)),
                "rating": RATING_MAP.get(rating_word),
                "availability": availability,
                "url": urljoin(page_url, link["href"]),
            }
        )

    next_link = soup.select_one("li.next a")
    next_url = urljoin(page_url, next_link["href"]) if next_link else None
    return books, next_url


def main():
    all_books = []
    url = START_URL
    page_number = 1

    with requests.Session() as session:
        while url:
            print(f"Scraping page {page_number}: {url}")
            html = fetch(url, session)
            books, url = parse_page(html, url)
            all_books.extend(books)
            page_number += 1
            time.sleep(DELAY_SECONDS)

    df = pd.DataFrame(all_books)
    df = df.drop_duplicates(subset="url").reset_index(drop=True)

    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_DIR / "books.csv", index=False, encoding="utf-8-sig")
    df.to_excel(OUTPUT_DIR / "books.xlsx", index=False)

    print(f"\nDone! {len(df)} books saved to the '{OUTPUT_DIR}' folder.")
    print(f"Average price: £{df['price_gbp'].mean():.2f}")


if __name__ == "__main__":
    main()
