import os
import json
import re
from openai import OpenAI
# from config_agent2 import OPENAI_API_KEY, RESUME_DIR, JOB_DESC_DIR, OUTPUT_DIR
# from utils_agent2 import read_resume
# from logging_agent2 import logger

from app.core.config_agent2 import OPENAI_API_KEY, RESUME_DIR, JOB_DESC_DIR, OUTPUT_DIR
from app.core.utils_agent2 import read_resume
from app.core.logging_agent2 import logger


# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_resume_analysis(job_desc_file: str, resume_file: str) -> dict:
    """Compare resume with job description and generate insights"""
    # Load job description
    job_path = os.path.join(JOB_DESC_DIR, job_desc_file)
    if not os.path.exists(job_path):
        raise FileNotFoundError(f"Job description file not found: {job_path}")

    with open(job_path, "r", encoding="utf-8") as f:
        job_desc = json.load(f)

    # Read resume
    resume_text = read_resume(resume_file, RESUME_DIR)

    # Prepare OpenAI prompt
    prompt = f"""
    You are an AI career assistant. Compare the candidate's resume with the job description.
    
    Job Description:
    {json.dumps(job_desc, indent=4)}

    Candidate Resume:
    {resume_text}

    Output JSON with:
    - Key Skills Required
    - Matching Strengths
    - Missing / Less-Emphasized Skills
    - Interview Preparation Guidance:
        * Suggested self-introduction points
        * Likely interview questions
        * Recommended talking points
        * Questions to ask the interviewer
    """

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides structured resume-job analysis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    # Extract and clean response
    text_response = response.choices[0].message.content.strip()
    text_response = re.sub(r"^```json\s*|\s*```$", "", text_response, flags=re.DOTALL).strip()

    try:
        data = json.loads(text_response)
    except json.JSONDecodeError:
        data = {"analysis": text_response}

    # Save JSON output
    output_file = os.path.join(OUTPUT_DIR, f"{resume_file}_analysis.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    logger.info(f"Resume analysis saved at {output_file}")
    return data

def main():
    print("===== AI Resume-Job Analysis (Agent 2) =====")
    resume_file = input("Enter resume filename (from data/resumes/): ").strip()
    job_desc_file = input("Enter job description filename (from data/job_descriptions/): ").strip()

    if not resume_file or not job_desc_file:
        print("Resume or Job Description file not provided. Exiting...")
        return

    result = generate_resume_analysis(job_desc_file, resume_file)
    print("\nResume-Job Analysis Output:\n")
    print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
