import os
import json
import re
from openai import OpenAI
from backend.app.core.config import OPENAI_API_KEY, OUTPUT_DIR
from backend.app.core.utils import scrape_job_description
from backend.app.core.logging import logger

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def refine_with_openai(structured_data: dict) -> dict:
    """
    Optional: send Docling output to OpenAI to standardize and enrich JSON.
    """
    prompt = f"""
    Here is a structured job description extracted from a job posting:

    {json.dumps(structured_data, indent=4)}

    Please clean, standardize, and enrich this data. 
    Return JSON with fields: Job Title, Company, Location, Experience Level, Required Skills, 
    Nice-to-Have Skills, Responsibilities, Tools & Technologies, Role Summary, KPIs, Interview Notes, Key Challenges, Company Culture & Values, Compensation/Benefits (if mentioned).
    Make sure the JSON is well-formatted, human-readable, and includes as many details as possible inferred from the job posting. 
    Do not return markdown code blocks, return plain JSON only.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that formats job data cleanly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        text_response = completion.choices[0].message.content.strip()
        cleaned_text = re.sub(r"^```json\s*|\s*```$", "", text_response, flags=re.DOTALL).strip()

        return json.loads(cleaned_text)
    except Exception as e:
        logger.error(f"OpenAI refinement failed: {e}")
        return {"structured_description": structured_data, "note": "OpenAI refinement failed"}

def process_job_url(job_url: str) -> dict:
    """
    Main pipeline: scrape job description, structure with Docling, refine with OpenAI, save JSON.
    """
    logger.info(f"Processing job URL: {job_url}")
    try:
        # Scrape + structure with Docling
        structured_data = scrape_job_description(job_url)

        # Refine/enrich with OpenAI (optional)
        final_data = refine_with_openai(structured_data)

        # Save output
        output_path = os.path.join(OUTPUT_DIR, "output.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

        logger.info(f"Output saved to {output_path}")
        return final_data
    except Exception as e:
        logger.error(f"Error processing job URL: {e}")
        return {"error": str(e)}

def main():
    print("===== AI Job Description Analyzer =====")
    job_url = input("Enter the Job Posting URL: ").strip()
    if not job_url:
        print("No URL entered. Exiting...")
        return

    result = process_job_url(job_url)
    print("Structured Job Description saved to data/job_description/output.json")
    # print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()





