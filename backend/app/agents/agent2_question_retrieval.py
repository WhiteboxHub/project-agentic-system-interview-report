# project-agentic-system-interview-report/backend/app/agents/agent2_question_retrieval.py
import os
import json
import re
from openai import OpenAI

# from config_agent2 import OPENAI_API_KEY, RESUME_DIR, JOB_DESC_DIR, OUTPUT_DIR
# from utils_agent2 import read_resume
# from logging_agent2 import logger

from backend.app.core.config_agent2 import (
    OPENAI_API_KEY,
    RESUME_DIR,
    JOB_DESC_DIR,
    OUTPUT_DIR,
)
from backend.app.core.utils_agent2 import read_resume
from backend.app.core.logging_agent2 import logger


# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_resume_analysis(job_desc_file: str, resume_file: str) -> dict:
    """Enhanced resume analysis with comprehensive interview preparation guidance"""
    # Load job description
    job_path = os.path.join(JOB_DESC_DIR, job_desc_file)
    if not os.path.exists(job_path):
        raise FileNotFoundError(f"Job description file not found: {job_path}")

    with open(job_path, "r", encoding="utf-8") as f:
        job_desc = json.load(f)

    # Read resume
    resume_text = read_resume(resume_file, RESUME_DIR)

    # Enhanced OpenAI prompt for comprehensive analysis
    prompt = f"""
    You are an expert career coach and interview preparation specialist. Analyze this candidate's resume against the job description and create a comprehensive 10+ page interview preparation report.

    JOB DESCRIPTION:
    {json.dumps(job_desc, indent=4)}

    CANDIDATE RESUME:
    {resume_text}

    Create a detailed JSON analysis with the following sections:

    1. EXECUTIVE SUMMARY:
       - Overall Match Percentage (0-100%)
       - Key Strengths Summary
       - Primary Concerns/Gaps
       - Recommended Preparation Focus Areas

    2. SKILLS ANALYSIS:
       - Required Skills Assessment (match/missing/partial)
       - Technical Skills Gap Analysis
       - Soft Skills Evaluation
       - Certifications & Education Alignment
       - Experience Level Comparison

    3. PERSONALIZED INTRODUCTION STRATEGY:
       - 30-Second Elevator Pitch Template
       - 2-Minute Detailed Introduction
       - Key Value Propositions to Highlight
       - Unique Selling Points
       - Career Story Narrative

    4. TECHNICAL PREPARATION:
       - Technical Skills to Brush Up On
       - Coding Challenges to Practice
       - System Design Topics
       - Architecture Questions to Study
       - Tools & Technologies to Research
       - Portfolio Projects to Highlight

    5. BEHAVIORAL PREPARATION:
       - STAR Method Examples to Prepare
       - Leadership Stories
       - Problem-Solving Examples
       - Teamwork Scenarios
       - Failure & Learning Stories
       - Success Stories Relevant to Role

    6. INTERVIEW QUESTIONS BANK:
       - Technical Questions (20+ questions)
       - Behavioral Questions (15+ questions)
       - Company-Specific Questions (10+ questions)
       - Role-Specific Questions (10+ questions)
       - Situational Questions (10+ questions)

    7. QUESTIONS TO ASK INTERVIEWER:
       - Technical Questions (10+ questions)
       - Team & Culture Questions (10+ questions)
       - Growth & Development Questions (10+ questions)
       - Role-Specific Questions (10+ questions)

    8. KEYWORDS & PHRASES:
       - Technical Keywords to Use
       - Industry-Specific Terms
       - Company Values to Reference
       - Action Verbs to Include
       - Metrics & Achievements to Highlight

    9. RED FLAGS & CONCERNS:
       - Potential Weaknesses to Address
       - Gaps to Explain Proactively
       - Difficult Questions to Prepare For
       - Salary Negotiation Points
       - Timeline Concerns

    10. SUCCESS STRATEGIES:
        - Interview Day Preparation
        - Body Language Tips
        - Communication Style Adjustments
        - Follow-up Strategy
        - Negotiation Preparation

    11. COMPANY RESEARCH POINTS:
        - Recent Company News
        - Products/Services to Mention
        - Competitors to Reference
        - Industry Trends to Discuss
        - Company Culture Insights

    12. ROLE-SPECIFIC PREPARATION:
        - Daily Responsibilities Understanding
        - Team Dynamics Preparation
        - Tools & Processes to Learn
        - Metrics & KPIs to Know
        - Challenges to Anticipate

    Return ONLY valid JSON format. Make this comprehensive and actionable for interview preparation.
    """

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that provides structured resume-job analysis.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    # Extract and clean response
    text_response = response.choices[0].message.content.strip()
    text_response = re.sub(
        r"^```json\s*|\s*```$", "", text_response, flags=re.DOTALL
    ).strip()

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
    job_desc_file = input(
        "Enter job description filename (from data/job_descriptions/): "
    ).strip()

    if not resume_file or not job_desc_file:
        print("Resume or Job Description file not provided. Exiting...")
        return

    result = generate_resume_analysis(job_desc_file, resume_file)
    print("\nResume-Job Analysis Output:\n")
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
