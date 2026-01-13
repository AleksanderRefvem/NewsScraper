# News Scraper

A Python CLI tool that aggregates headlines from trusted international news sources via RSS feeds.

## Sources

- BBC World
- NPR
- The Guardian
- Al Jazeera
- Reuters (via Google News)
- AP News (via Google News)

## Installation

### Bash (Linux/macOS)
```bash
cd NewsScraper

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### PowerShell (Windows)
```powershell
cd NewsScraper

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

> **Note:** If you get an execution policy error, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

## Usage

### Bash (Linux/macOS)
```bash
source venv/bin/activate

# Fetch latest news from all sources
python -m src.main fetch

# View latest headlines
python -m src.main headlines

# View last 10 headlines
python -m src.main headlines -n 10

# Filter by source
python -m src.main headlines -s "BBC World"
```

### PowerShell (Windows)
```powershell
.\venv\Scripts\Activate.ps1

# Fetch latest news from all sources
python -m src.main fetch

# View latest headlines
python -m src.main headlines

# View last 10 headlines
python -m src.main headlines -n 10

# Filter by source
python -m src.main headlines -s "BBC World"
```

### Alternative: Run from src directory
```bash
cd src
python main.py fetch
python main.py headlines
```

## Project Structure
```
NewsScraper/
├── src/
│   ├── main.py       # CLI entry point
│   ├── config.py     # RSS feed URLs and settings
│   ├── database.py   # SQLite operations
│   ├── fetcher.py    # RSS feed parsing
│   ├── models.py     # Article dataclass
│   └── utils.py      # Helper functions
├── data/
│   └── news.db       # SQLite database (created on first run)
├── requirements.txt
└── README.md
```

## Dependencies

- `feedparser` - RSS/Atom feed parsing
- `requests` - HTTP client
- `python-dateutil` - Date parsing
