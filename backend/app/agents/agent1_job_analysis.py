import json
import os
import re
from openai import OpenAI
from backend.app.core.config import OPENAI_API_KEY, OUTPUT_DIR
from backend.app.core.utils import scrape_job_description
from backend.app.core.logging import logger

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def clean_with_openai(raw_text: str) -> dict:
    """Send raw job text to OpenAI and get structured JSON back."""
    prompt = f"""
        Extract detailed and structured information from the following job description.

        Return JSON with the following fields:

        - Job Title
        - Company
        - Location
        - Experience Level
        - Required Skills (with proficiency if mentioned)
        - Responsibilities (list all clearly)
        - Nice-to-Have Skills
        - Tools & Technologies
        - Role Summary (2-3 sentences describing the role)
        - Key Performance Indicators / Success Metrics (if mentioned)
        - Interview Preparation Notes (any hints or context from the description)

        Make the JSON clean, readable, and indented.
        Do NOT wrap JSON in markdown backticks.

        Job Description:
        {raw_text}
        """


    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that formats job data cleanly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    text_response = completion.choices[0].message.content.strip()

    # Remove Markdown code block formatting ```json ... ```
    cleaned_text = re.sub(r"^```json\s*|\s*```$", "", text_response, flags=re.DOTALL).strip()

    try:
        # Convert string JSON into proper Python dict
        data = json.loads(cleaned_text)
    except json.JSONDecodeError:
        # If still fails, return raw text
        data = {"structured_description": cleaned_text}

    return data

def process_job_url(job_url: str) -> dict:
    """Main pipeline: scrape, clean, and save output."""
    logger.info(f"Processing job URL: {job_url}")
    try:
        raw_text = scrape_job_description(job_url)
        cleaned = clean_with_openai(raw_text)
        output_path = os.path.join(OUTPUT_DIR, "output.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=4, ensure_ascii=False)

        logger.info(f"Output saved to {output_path}")
        return cleaned
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}

def main():
    print("===== AI Job Description Analyzer =====")
    job_url = input("Enter the Job Posting URL: ").strip()

    if not job_url:
        print("No URL entered. Exiting...")
        return

    result = process_job_url(job_url)
    print("\nStructured Job Description:\n")
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    print("Result saved to output.json")

if __name__ == "__main__":
    main()
