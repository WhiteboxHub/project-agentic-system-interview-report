# project-agentic-system-interview-report/backend/app/core/utils.py
import requests
from bs4 import BeautifulSoup
from docling.datamodel.document import DoclingDocument
from backend.app.core.logging import logger
import re
import time


def scrape_job_description(url: str) -> dict:
    """
    Enhanced job posting scraper with better text extraction and cleaning.
    Uses multiple strategies to extract clean, relevant job description text.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove unwanted elements
        for tag in soup(
            ["script", "style", "noscript", "nav", "header", "footer", "aside"]
        ):
            tag.extract()

        # Try to find job-specific content areas
        job_content_selectors = [
            '[class*="job-description"]',
            '[class*="job-content"]',
            '[class*="description"]',
            '[class*="requirements"]',
            '[class*="responsibilities"]',
            '[id*="job-description"]',
            '[id*="description"]',
            "main",
            "article",
            ".content",
        ]

        job_text = ""
        for selector in job_content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    job_text += element.get_text() + "\n"
                break

        # If no specific job content found, use all text
        if not job_text.strip():
            job_text = soup.get_text()

        # Clean and structure the text
        cleaned_text = clean_job_text(job_text)

        # Structure the data for DoclingDocument
        doc_data = {
            "name": "job_posting",
            "content": cleaned_text,
            "metadata": {
                "source_url": url,
                "content_type": "job_posting",
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "text_length": len(cleaned_text),
            },
        }

        doc = DoclingDocument(**doc_data)
        structured_data = doc.dict()

        return {
            "job_description": cleaned_text,
            "structured_data": structured_data,
            "raw_text": job_text,
            "url": url,
        }

    except requests.RequestException as e:
        logger.error(f"HTTP error while fetching URL {url}: {e}")
        return {"error": f"HTTP error: {e}"}
    except Exception as e:
        logger.error(f"Error processing job description: {e}")
        return {"error": str(e)}


def clean_job_text(text: str) -> str:
    """
    Clean and normalize job description text for better processing.
    """
    # Remove extra whitespace and normalize
    text = re.sub(r"\s+", " ", text)

    # Remove common job board noise
    noise_patterns = [
        r"Apply now.*?",
        r"Click here.*?",
        r"Powered by.*?",
        r"©.*?",
        r"All rights reserved.*?",
        r"Privacy policy.*?",
        r"Terms of service.*?",
        r"Cookie policy.*?",
        r"Subscribe.*?",
        r"Follow us.*?",
        r"Share this.*?",
        r"Report this job.*?",
        r"Save job.*?",
        r"Email job.*?",
    ]

    for pattern in noise_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

    # Remove excessive punctuation
    text = re.sub(r"[.]{3,}", "...", text)
    text = re.sub(r"[-]{3,}", "---", text)

    # Clean up line breaks and spacing
    text = re.sub(r"\n\s*\n", "\n\n", text)
    text = text.strip()

    return text
