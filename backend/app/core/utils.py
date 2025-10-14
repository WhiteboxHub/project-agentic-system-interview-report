import requests
from bs4 import BeautifulSoup

def scrape_job_description(url: str) -> str:
    """Fetch and extract main text content from a job posting URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    # Extract visible text
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()
    text = " ".join(soup.get_text().split())
    return text
