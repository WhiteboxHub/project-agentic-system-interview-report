# project-agentic-system-interview-report/backend/app/agents/agent1_job_analysis.py
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
    Enhanced OpenAI analysis to extract comprehensive job information.
    """
    job_text = structured_data.get("job_description", "")

    prompt = f"""
    You are an expert job description analyst. Analyze this job posting and extract comprehensive information.

    JOB POSTING TEXT:
    {job_text}

    Extract and structure the following information into a detailed JSON format:

    1. BASIC INFORMATION:
       - Job Title (exact title)
       - Company Name
       - Location (city, state, country, remote/hybrid/onsite)
       - Experience Level (entry/mid/senior/staff/principal)
       - Employment Type (full-time/part-time/contract)
       - Salary Range (if mentioned)

    2. TECHNICAL REQUIREMENTS:
       - Required Skills (programming languages, frameworks, tools)
       - Nice-to-Have Skills (preferred but not mandatory)
       - Tools & Technologies (specific software, platforms, systems)
       - Certifications Required
       - Years of Experience Required

    3. ROLE DETAILS:
       - Key Responsibilities (detailed list)
       - Daily Tasks
       - Team Structure (who they'll work with)
       - Reporting Structure
       - Growth Opportunities

    4. COMPANY INFORMATION:
       - Company Size
       - Industry
       - Company Culture & Values
       - Mission Statement
       - Benefits & Perks
       - Work Environment

    5. INTERVIEW PREPARATION INSIGHTS:
       - Likely Technical Interview Topics
       - Behavioral Questions to Expect
       - Skills Assessment Areas
       - Portfolio/Project Requirements
       - Key Metrics/KPIs for Success

    6. CANDIDATE PROFILE:
       - Ideal Candidate Description
       - Educational Requirements
       - Soft Skills Needed
       - Leadership Requirements
       - Communication Skills

    Return ONLY valid JSON format. Do not include markdown code blocks or any other text.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that formats job data cleanly.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        text_response = completion.choices[0].message.content.strip()
        cleaned_text = re.sub(
            r"^```json\s*|\s*```$", "", text_response, flags=re.DOTALL
        ).strip()

        return json.loads(cleaned_text)
    except Exception as e:
        logger.error(f"OpenAI refinement failed: {e}")
        return {
            "structured_description": structured_data,
            "note": "OpenAI refinement failed",
        }


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
