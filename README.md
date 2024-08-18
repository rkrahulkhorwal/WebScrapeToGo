# WebScrapeToGo

WebScrapeToGo is a Python-based web scraping tool that allows users to scrape content from multiple URLs, optionally use proxies, and generate a PDF report of the scraped content.

## Features

- Scrape content from multiple URLs
- Optional proxy support with rotation
- Content cleaning to remove non-Latin1 characters
- PDF report generation of scraped content
- Random delays between requests to avoid rate limiting

## Requirements

- Python 3.x
- cloudscraper
- beautifulsoup4
- fpdf

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/rkrahulkhorwal/WebScrapeToGo.git
   cd WebScrapeToGo
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```
   python webscrape_to_go.py
   ```

2. When prompted, enter the URLs you want to scrape, separated by commas.

3. Optionally, provide the path to a proxy file. If you don't want to use proxies, just press Enter.

4. The script will scrape the provided URLs and generate a PDF report named `scraped_url_contents.pdf` in the same directory.

## Proxy File Format

If you choose to use proxies, your proxy file should have one proxy per line in the following format:

```
ip:port:username:password
```

## Limitations

- The script currently limits the content in the PDF to the first 100 lines per URL to prevent excessively large files.
- The content scraping method is simple and may need adjustment for websites with different structures.

## Disclaimer

This tool is for educational purposes only. Always respect websites' terms of service and robots.txt files when scraping. Use responsibly and ethically.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/WebScrapeToGo/issues) if you want to contribute.
