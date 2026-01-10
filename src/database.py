import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from .config import DATABASE_PATH
    from .models import Article
except ImportError:
    from config import DATABASE_PATH
    from models import Article


def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT,
            url TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            published_date TIMESTAMP,
            category TEXT,
            fetched_at TIMESTAMP NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_source ON articles(source)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_published ON articles(published_date)")
    conn.commit()
    conn.close()


def insert_article(article: Article) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO articles (title, summary, url, source, published_date, category, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                article.title,
                article.summary,
                article.url,
                article.source,
                article.published_date,
                article.category,
                article.fetched_at,
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Duplicate URL
    finally:
        conn.close()


def get_latest_articles(limit: int = 20, source: Optional[str] = None) -> list[Article]:
    conn = get_connection()
    cursor = conn.cursor()

    if source:
        cursor.execute(
            """
            SELECT * FROM articles
            WHERE source = ?
            ORDER BY published_date DESC
            LIMIT ?
            """,
            (source, limit),
        )
    else:
        cursor.execute(
            """
            SELECT * FROM articles
            ORDER BY published_date DESC
            LIMIT ?
            """,
            (limit,),
        )

    rows = cursor.fetchall()
    conn.close()

    return [
        Article(
            title=row["title"],
            summary=row["summary"],
            url=row["url"],
            source=row["source"],
            published_date=datetime.fromisoformat(row["published_date"]) if row["published_date"] else None,
            category=row["category"],
            fetched_at=datetime.fromisoformat(row["fetched_at"]) if row["fetched_at"] else None,
        )
        for row in rows
    ]


def get_article_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles")
    count = cursor.fetchone()[0]
    conn.close()
    return count
