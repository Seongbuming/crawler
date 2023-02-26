# default-scraper

Python Web Scraper

## Features

- Scrap all search results for a keyword entered as an argument.
- Can be save as `.csv` and `.json`.
- Also collect user data who uploaded contents included in search results.

## Usage

### Install

```bash
pip install default-scraper
```

or

```bash
pip install git+https://github.com/Seongbuming/crawler.git
```

### Scrap Instagram contents in python script

```python
from default_scraper.instagram.parser import InstagramParser
USERNAME = ""
PASSWORD = ""
KEYWORD = ""
parser = InstagramParser(USERNAME, PASSWORD, KEYWORD, False)
parser.run()
```

### Scrap Instagram contents using bash command

Run following command to scrap contents from Instagram:

```bash
python main.py --platform instagram --keyword {KEYWORD} [--output_file OUTPUT_FILE] [--all]
```

Use `--all` or `-a` option to also scrap unstructured fields.

### Scrap Google Play Store reviews in python script

```python
from default_scraper.googleplay.review.parser import GooglePlayReviewParser
APP_ID = ""
parser = GooglePlayReviewParser(APP_ID)
parser.run()
```

### Scrap Google Play Store reviews using bash command

```bash
python main.py --platform googleplay_review --keyword {APP_ID} [--output_file OUTPUT_FILE]
```

## Data description

### Instagram

- Structured fields
  - `pk`
  - `id`
  - `taken_at`
  - `media_type`
  - `code`
  - `comment_count`
  - `user`
  - `like_count`
  - `caption`
  - `accessibility_caption`
  - `original_width`
  - `original_height`
  - `images`
- Some fields may be missing depending on Instagram's response data.

### Google Play Store Review

- `review_id`
- `author`
- `review_text`
- `rating`
- `writed_time`

## Future works

- Will support scraping from more platform services.
