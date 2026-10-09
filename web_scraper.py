"""
CodeAlpha Data Analytics Internship
Task 1: Web Scraping

Website:
https://quotes.toscrape.com/

Purpose:
Scrape public quote data using Requests + BeautifulSoup,
handle pagination, clean the data, and save it as CSV.
"""

import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
OUTPUT_FILE = Path("outputs/quotes_dataset.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CodeAlphaStudentProject/1.0)"
}


def scrape_quotes(start_url=BASE_URL, max_pages=10):
    """Scrape quote records from the public practice website."""
    records = []
    current_url = start_url
    visited_urls = set()

    for page_number in range(1, max_pages + 1):
        if current_url in visited_urls:
            break

        visited_urls.add(current_url)

        print(f"Scraping page {page_number}: {current_url}")

        response = requests.get(
            current_url,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        quote_blocks = soup.select("div.quote")

        # Stop if there are no quote records.
        if not quote_blocks:
            break

        for block in quote_blocks:
            quote_element = block.select_one("span.text")
            author_element = block.select_one("small.author")
            author_link = block.select_one("span a")
            tag_elements = block.select("a.tag")

            quote_text = (
                quote_element.get_text(strip=True)
                if quote_element else ""
            )

            author = (
                author_element.get_text(strip=True)
                if author_element else ""
            )

            author_url = ""
            if author_link and author_link.get("href"):
                author_url = urljoin(current_url, author_link["href"])

            tags = ", ".join(
                tag.get_text(strip=True)
                for tag in tag_elements
            )

            records.append({
                "quote": quote_text,
                "author": author,
                "tags": tags,
                "author_url": author_url,
                "source_page": current_url
            })

        # Find the Next button.
        next_link = soup.select_one("li.next a")

        if not next_link or not next_link.get("href"):
            break

        current_url = urljoin(current_url, next_link["href"])

        # Polite delay between requests.
        time.sleep(1)

    return records


def clean_data(records):
    """Convert scraped records into a clean DataFrame."""
    df = pd.DataFrame(records)

    if df.empty:
        return df

    # Remove duplicate quotes.
    df = df.drop_duplicates(subset=["quote"]).copy()

    # Remove unnecessary whitespace.
    for column in ["quote", "author", "tags", "author_url", "source_page"]:
        df[column] = df[column].astype(str).str.strip()

    # Useful derived field for analysis.
    df["quote_length"] = df["quote"].str.len()

    return df


def main():
    records = scrape_quotes()
    df = clean_data(records)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print("\n===== SCRAPING COMPLETE =====")
    print("Total records:", len(df))
    print("Columns:", list(df.columns))
    print("\nFirst 5 records:")
    print(df.head().to_string(index=False))
    print(f"\nDataset saved to: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
