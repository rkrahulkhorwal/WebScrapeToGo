import cloudscraper
import random
from bs4 import BeautifulSoup
from fpdf import FPDF
import textwrap
import os
import time
import re

def load_proxies(file_path):
    if not file_path or not os.path.exists(file_path):
        print(f"Proxy file not found or not specified. Proceeding without proxies.")
        return None

    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]

    if not proxies:
        print("Proxy file is empty. Proceeding without proxies.")
        return None

    return proxies

def get_random_proxy(proxy_list):
    return random.choice(proxy_list) if proxy_list else None

def create_scraper(proxy=None):
    scraper = cloudscraper.create_scraper()
    if proxy:
        ip, port, username, password = proxy.split(':')
        scraper.proxies = {
            'http': f'http://{username}:{password}@{ip}:{port}',
            'https': f'http://{username}:{password}@{ip}:{port}'
        }
    return scraper

def scrape_website_content(url, proxy_list=None):
    try:
        scraper = create_scraper(get_random_proxy(proxy_list))
        response = scraper.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.title.string if soup.title else "No title found"

        # Extract main content (this is a simple approach and might need adjustment for different site structures)
        content = ""
        for paragraph in soup.find_all('p'):
            content += paragraph.get_text() + "\n\n"

        return title, content.strip()
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return "Error", f"Failed to scrape content: {str(e)}"

def clean_text(text):
    # Remove emojis and other non-Latin1 characters
    return re.sub(r'[^\u0000-\u00FF]', '', text)

def create_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Scraped URL Contents", ln=1, align='C')
    pdf.ln(10)

    for i, (url, title, content) in enumerate(results, 1):
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt=f"URL {i}: {clean_text(url)}", ln=1)
        pdf.ln(5)

        pdf.set_font("Arial", 'B', size=11)
        pdf.cell(200, 10, txt=f"Title: {clean_text(title)}", ln=1)
        pdf.ln(5)

        pdf.set_font("Arial", size=10)
        cleaned_content = clean_text(content)
        content_lines = textwrap.wrap(cleaned_content, width=90)
        for line in content_lines[:100]:  # Limit to first 100 lines
            pdf.cell(0, 10, txt=line, ln=1)

        if len(content_lines) > 100:
            pdf.cell(0, 10, txt="...(content truncated)...", ln=1)

        pdf.ln(10)

    pdf_filename = "scraped_url_contents.pdf"
    pdf.output(pdf_filename)
    print(f"Results saved to {pdf_filename}")

def main(urls, proxy_file):
    proxy_list = load_proxies(proxy_file)
    all_results = []

    for i, url in enumerate(urls, 1):
        print(f"Scraping content from URL {i}: {url}")
        title, content = scrape_website_content(url, proxy_list=proxy_list)
        print(f"Title: {title}")
        print(f"Content length: {len(content)} characters")
        print("-" * 50)
        all_results.append((url, title, content))
        time.sleep(random.uniform(1, 3))  # Random delay between requests

    create_pdf(all_results)

if __name__ == "__main__":
    urls = input("Enter the URLs to scrape (comma-separated): ").split(',')
    urls = [url.strip() for url in urls]  # Remove any leading/trailing whitespace
    proxy_file = input("Enter the path to your proxy file (or press Enter to skip): ")
    main(urls, proxy_file)
