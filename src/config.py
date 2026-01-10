from pathlib import Path

# Database configuration
DATA_DIR = Path(__file__).parent.parent / "data"
DATABASE_PATH = DATA_DIR / "news.db"

# RSS Feed sources
# Trusted international news sources known for objective reporting
RSS_FEEDS = {
    "Reuters": "https://news.google.com/rss/search?q=site:reuters.com&hl=en-US&gl=US&ceid=US:en",
    "AP News": "https://news.google.com/rss/search?q=site:apnews.com&hl=en-US&gl=US&ceid=US:en",
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
}

# Fetching settings
REQUEST_TIMEOUT = 30  # seconds
USER_AGENT = "NewsScraper/1.0 (Educational Project)"
