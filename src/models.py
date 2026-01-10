from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    title: str
    summary: str
    url: str
    source: str
    published_date: Optional[datetime]
    category: Optional[str] = None
    fetched_at: Optional[datetime] = None

    def __post_init__(self):
        if self.fetched_at is None:
            self.fetched_at = datetime.utcnow()
