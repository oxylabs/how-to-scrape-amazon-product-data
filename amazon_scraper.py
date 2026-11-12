"""
Template Amazon product scraper, built from the steps in README.md.

Usage:
    python amazon_scraper.py "<amazon_search_or_category_url>"
    python amazon_scraper.py "<amazon_search_or_category_url>" --output products.csv --max-pages 3
"""

import argparse
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

DEFAULT_OUTPUT_FILE = "amazon_products.csv"

CUSTOM_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Accept-Language": "da, en-gb, en",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
}


def get_product_info(url: str) -> dict | None:
    """Scrapes name, price, rating, image, and description from a product page."""
    response = requests.get(url, headers=CUSTOM_HEADERS)
    if response.status_code != 200:
        print(f"Error in getting webpage: {url}")
        return None

    soup = BeautifulSoup(response.text, "lxml")

    title_element = soup.select_one("#productTitle")
    title = title_element.text.strip() if title_element else None

    price_element = soup.select_one("span.a-offscreen")
    price = price_element.text if price_element else None

    rating_element = soup.select_one("#acrPopover")
    rating_text = rating_element.attrs.get("title") if rating_element else None
    rating = rating_text.replace("out of 5 stars", "") if rating_text else None

    image_element = soup.select_one("#landingImage")
    image = image_element.attrs.get("src") if image_element else None

    description_element = soup.select_one("#productDescription")
    description = description_element.text.strip() if description_element else None

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "image": image,
        "description": description,
        "url": url,
    }


def parse_listing(listing_url: str, visited_urls: set, max_pages: int, page: int = 1) -> list[dict]:
    """Walks a search/category listing page (and its pagination) and scrapes each product."""
    response = requests.get(listing_url, headers=CUSTOM_HEADERS)
    print(f"[page {page}] {response.status_code} {listing_url[:100]}")
    soup_search = BeautifulSoup(response.text, "lxml")
    result_cards = soup_search.select('div[data-component-type="s-search-result"][data-asin]')
    page_data = []

    for card in result_cards:
        asin = card.get("data-asin")
        full_url = urljoin(listing_url, f"/dp/{asin}")
        if full_url not in visited_urls:
            visited_urls.add(full_url)
            print(f"Scraping product from {full_url[:100]}", flush=True)
            product_info = get_product_info(full_url)
            if product_info:
                page_data.append(product_info)

    next_page_el = soup_search.select_one("a.s-pagination-next")
    if next_page_el and page < max_pages:
        next_page_url = urljoin(listing_url, next_page_el.attrs.get("href"))
        page_data += parse_listing(next_page_url, visited_urls, max_pages, page + 1)

    return page_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Amazon product data from a search or category page.")
    parser.add_argument("url", help="Amazon search results or category page URL")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_FILE, help=f"CSV file to write to (default: {DEFAULT_OUTPUT_FILE})")
    parser.add_argument("--max-pages", type=int, default=1, help="Maximum number of listing pages to follow (default: 1)")
    args = parser.parse_args()

    visited_urls: set = set()
    data = parse_listing(args.url, visited_urls, args.max_pages)

    df = pd.DataFrame(data)
    df.to_csv(args.output, index=False)
    print(f"Wrote {len(data)} products to {args.output}")


if __name__ == "__main__":
    main()
