"""Small web-scraping exercise for Unit 3.

The script retrieves the Wikipedia Data science page, extracts paragraphs
containing the phrase "data scientist", and stores the result as JSON.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


SOURCE_URL = "https://en.wikipedia.org/wiki/Data_science"
KEYWORD = "data scientist"
OUTPUT_PATH = Path(__file__).with_name("web_scraping_results.json")


def clean_text(value: str) -> str:
    """Collapse whitespace and remove Wikipedia's numbered citations."""
    value = re.sub(r"\[\s*\d+\s*\]", "", value)
    value = " ".join(value.split())
    return re.sub(r"\s+([,.;:!?])", r"\1", value)


def scrape_paragraphs(url: str, keyword: str) -> dict[str, object]:
    """Return page paragraphs containing *keyword* (case-insensitive)."""
    headers = {
        "User-Agent": (
            "University coursework web-scraping exercise; "
            "single educational request"
        )
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    matches = []

    for paragraph in soup.select("p"):
        text = clean_text(paragraph.get_text(" ", strip=True))
        if text and keyword.casefold() in text.casefold():
            matches.append(text)

    return {
        "source_url": url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "http_status": response.status_code,
        "keyword": keyword,
        "match_count": len(matches),
        "matches": matches,
    }


def main() -> None:
    result = scrape_paragraphs(SOURCE_URL, KEYWORD)
    OUTPUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"HTTP status: {result['http_status']}")
    print(f"Paragraphs containing {KEYWORD!r}: {result['match_count']}")
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
