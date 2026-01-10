from datetime import datetime
from typing import Optional

import feedparser
import requests

try:
    from .config import REQUEST_TIMEOUT, RSS_FEEDS, USER_AGENT
    from .models import Article
    from .utils import parse_date, clean_html
except ImportError:
    from config import REQUEST_TIMEOUT, RSS_FEEDS, USER_AGENT
    from models import Article
    from utils import parse_date, clean_html


def fetch_feed(url: str) -> Optional[feedparser.FeedParserDict]:
    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        )
        response.raise_for_status()
        return feedparser.parse(response.content)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_feed_entries(feed: feedparser.FeedParserDict, source: str) -> list[Article]:
    articles = []

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        if not title:
            continue

        summary = entry.get("summary", "") or entry.get("description", "")
        summary = clean_html(summary)

        url = entry.get("link", "")
        if not url:
            continue

        published_date = parse_date(entry)

        category = None
        if "tags" in entry and entry.tags:
            category = entry.tags[0].get("term", None)

        articles.append(
            Article(
                title=title,
                summary=summary,
                url=url,
                source=source,
                published_date=published_date,
                category=category,
            )
        )

    return articles


def fetch_all_feeds() -> list[Article]:
    all_articles = []

    for source, url in RSS_FEEDS.items():
        print(f"Fetching {source}...")
        feed = fetch_feed(url)

        if feed is None:
            print(f"  Failed to fetch {source}")
            continue

        articles = parse_feed_entries(feed, source)
        all_articles.extend(articles)
        print(f"  Found {len(articles)} articles")

    return all_articles
