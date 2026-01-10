import re
from datetime import datetime
from typing import Optional

from dateutil import parser as date_parser


def parse_date(entry: dict) -> Optional[datetime]:
    date_fields = ["published_parsed", "updated_parsed"]

    for field in date_fields:
        if field in entry and entry[field]:
            try:
                from time import mktime
                return datetime.fromtimestamp(mktime(entry[field]))
            except (ValueError, OverflowError):
                continue

    string_fields = ["published", "updated"]
    for field in string_fields:
        if field in entry and entry[field]:
            try:
                return date_parser.parse(entry[field])
            except (ValueError, TypeError):
                continue

    return None


def clean_html(text: str) -> str:
    if not text:
        return ""

    cleaned = re.sub(r"<[^>]+>", "", text)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip()

    return cleaned


def truncate(text: str, max_length: int = 200) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rsplit(" ", 1)[0] + "..."
