#!/usr/bin/env python3
import argparse
from datetime import datetime

try:
    from .database import init_db, insert_article, get_latest_articles, get_article_count
    from .fetcher import fetch_all_feeds
    from .utils import truncate
except ImportError:
    from database import init_db, insert_article, get_latest_articles, get_article_count
    from fetcher import fetch_all_feeds
    from utils import truncate


def fetch_command() -> None:
    print("Initializing database...")
    init_db()

    print("\nFetching news from all sources...\n")
    articles = fetch_all_feeds()

    new_count = 0
    for article in articles:
        if insert_article(article):
            new_count += 1

    total = get_article_count()
    print(f"\nDone! Added {new_count} new articles. Total in database: {total}")


def headlines_command(limit: int = 20, source: str = None) -> None:
    articles = get_latest_articles(limit=limit, source=source)

    if not articles:
        print("No articles found. Run 'fetch' first to populate the database.")
        return

    print(f"\n{'='*80}")
    print(f" LATEST HEADLINES")
    if source:
        print(f" Source: {source}")
    print(f"{'='*80}\n")

    for article in articles:
        date_str = article.published_date.strftime("%Y-%m-%d %H:%M") if article.published_date else "Unknown"
        print(f"[{article.source}] {date_str}")
        print(f"  {article.title}")
        if article.summary:
            print(f"  {truncate(article.summary, 100)}")
        print(f"  {article.url}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="News Scraper - Get headlines from trusted international sources"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Fetch command
    subparsers.add_parser("fetch", help="Fetch latest news from all sources")

    # Headlines command
    headlines_parser = subparsers.add_parser("headlines", help="Display latest headlines")
    headlines_parser.add_argument(
        "-n", "--limit", type=int, default=20, help="Number of headlines to show"
    )
    headlines_parser.add_argument(
        "-s", "--source", type=str, help="Filter by source name"
    )

    args = parser.parse_args()

    if args.command == "fetch":
        fetch_command()
    elif args.command == "headlines":
        headlines_command(limit=args.limit, source=args.source)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
