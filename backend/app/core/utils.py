import requests
from bs4 import BeautifulSoup
from docling.datamodel.document import DoclingDocument
from backend.app.core.logging import logger

def scrape_job_description(url: str) -> dict:
    """
    Fetch job posting URL, extract visible text, 
    and return structured job info using DoclingDocument.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove unwanted tags
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()
        raw_text = " ".join(soup.get_text().split())

        # Structure the data for DoclingDocument with required fields
        doc_data = {
            "name": "job_posting",  # Required field
            "content": raw_text,
            "metadata": {
                "source_url": url,
                "content_type": "job_posting"
            }
        }
        
        # Create DoclingDocument with the structured data
        doc = DoclingDocument(**doc_data)
        structured_data = doc.dict()

        return {"job_description": raw_text, "structured_data": structured_data}

    except requests.RequestException as e:
        logger.error(f"HTTP error while fetching URL {url}: {e}")
        return {"error": f"HTTP error: {e}"}
    except Exception as e:
        logger.error(f"Error processing job description: {e}")
        return {"error": str(e)}
