# Book Scraper (Python)

A simple web scraper that collects book data from the demo site
[books.toscrape.com](https://books.toscrape.com) and exports it to CSV and Excel.

## Features
- Handles pagination automatically (all pages)
- Extracts title, price, star rating, availability and product URL
- Retry logic for failed requests and a polite delay between requests
- Removes duplicates and cleans prices into numbers
- Exports to `output/books.csv` and `output/books.xlsx`

## Tech stack
Python, Requests, BeautifulSoup, Pandas

## How to run
```bash
pip install -r requirements.txt
python scraper.py
```

## Output columns
| Column | Description |
|---|---|
| title | Book title |
| price_gbp | Price in GBP (number) |
| rating | Star rating (1-5) |
| availability | Stock status |
| url | Link to the book page |

## Note
This project is for learning and portfolio purposes and uses a site made for scraping practice.
