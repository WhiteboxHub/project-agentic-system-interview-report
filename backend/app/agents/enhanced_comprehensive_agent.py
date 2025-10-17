# Enhanced Agentic Interview Preparation System
# Complete workflow agent that combines job analysis and resume analysis

import os
import json
import re
from openai import OpenAI
from backend.app.core.config_agent2 import (
    OPENAI_API_KEY,
    RESUME_DIR,
    JOB_DESC_DIR,
    OUTPUT_DIR,
)
from backend.app.core.utils_agent2 import read_resume
from backend.app.core.utils import scrape_job_description
from backend.app.core.logging_agent2 import logger
from jinja2 import Template

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_comprehensive_report(job_url: str, resume_file: str) -> dict:
    """
    Complete workflow: scrape job, analyze resume, generate comprehensive report
    """
    logger.info(f"Starting comprehensive analysis for job URL: {job_url}")

    try:
        # Step 1: Scrape and analyze job description
        logger.info("Step 1: Scraping job description...")
        job_data = scrape_job_description(job_url)

        if "error" in job_data:
            return {"error": f"Job scraping failed: {job_data['error']}"}

        # Step 2: Analyze job with OpenAI
        logger.info("Step 2: Analyzing job description with AI...")
        job_analysis = analyze_job_with_ai(job_data)

        # Step 3: Read resume
        logger.info("Step 3: Reading resume...")
        resume_text = read_resume(resume_file, RESUME_DIR)

        # Step 4: Generate comprehensive analysis
        logger.info("Step 4: Generating comprehensive analysis...")
        comprehensive_analysis = generate_comprehensive_analysis(
            job_analysis, resume_text, job_url
        )

        # Step 5: Generate HTML report
        logger.info("Step 5: Generating HTML report...")
        html_report = generate_html_report(job_analysis, comprehensive_analysis)

        # Step 6: Save all outputs
        logger.info("Step 6: Saving outputs...")
        save_outputs(job_analysis, comprehensive_analysis, html_report, resume_file)

        return {
            "success": True,
            "job_analysis": job_analysis,
            "resume_analysis": comprehensive_analysis,
            "html_report": html_report,
            "message": "Comprehensive report generated successfully",
        }

    except Exception as e:
        logger.error(f"Error in comprehensive report generation: {e}")
        return {"error": str(e)}


def analyze_job_with_ai(job_data: dict) -> dict:
    """Enhanced job analysis with comprehensive extraction"""
    job_text = job_data.get("job_description", "")

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

        job_analysis = json.loads(cleaned_text)
        job_analysis["scraped_at"] = job_data.get("metadata", {}).get("scraped_at", "")
        job_analysis["source_url"] = job_data.get("url", "")

        return job_analysis

    except Exception as e:
        logger.error(f"Job analysis failed: {e}")
        return {"error": f"Job analysis failed: {e}"}


def generate_comprehensive_analysis(
    job_analysis: dict, resume_text: str, job_url: str
) -> dict:
    """Generate comprehensive resume analysis with detailed preparation guidance"""

    prompt = f"""
    You are an expert career coach and interview preparation specialist. Analyze this candidate's resume against the job description and create a comprehensive interview preparation report.

    JOB DESCRIPTION:
    {json.dumps(job_analysis, indent=4)}

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

    try:
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

        text_response = response.choices[0].message.content.strip()
        text_response = re.sub(
            r"^```json\s*|\s*```$", "", text_response, flags=re.DOTALL
        ).strip()

        try:
            analysis = json.loads(text_response)
        except json.JSONDecodeError:
            analysis = {"analysis": text_response}

        return analysis

    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {e}")
        return {"error": f"Analysis failed: {e}"}


def generate_html_report(job_analysis: dict, resume_analysis: dict) -> str:
    """Generate HTML report using Jinja2 template"""
    try:
        # Read the template file
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "report_template.html"
        )
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Create Jinja2 template
        template = Template(template_content)

        # Render the template
        html_content = template.render(job=job_analysis, resume=resume_analysis)

        return html_content

    except Exception as e:
        logger.error(f"HTML report generation failed: {e}")
        return f"<html><body><h1>Report Generation Error</h1><p>{e}</p></body></html>"


def save_outputs(
    job_analysis: dict, resume_analysis: dict, html_report: str, resume_file: str
):
    """Save all outputs to appropriate directories"""
    try:
        # Save job analysis
        job_output_path = os.path.join(JOB_DESC_DIR, "enhanced_output.json")
        with open(job_output_path, "w", encoding="utf-8") as f:
            json.dump(job_analysis, f, indent=4, ensure_ascii=False)

        # Save resume analysis
        resume_output_path = os.path.join(
            OUTPUT_DIR, f"{resume_file}_comprehensive_analysis.json"
        )
        with open(resume_output_path, "w", encoding="utf-8") as f:
            json.dump(resume_analysis, f, indent=4, ensure_ascii=False)

        # Save HTML report
        html_output_path = os.path.join(
            OUTPUT_DIR, f"{resume_file}_comprehensive_report.html"
        )
        with open(html_output_path, "w", encoding="utf-8") as f:
            f.write(html_report)

        logger.info(f"All outputs saved successfully")
        logger.info(f"Job analysis: {job_output_path}")
        logger.info(f"Resume analysis: {resume_output_path}")
        logger.info(f"HTML report: {html_output_path}")

    except Exception as e:
        logger.error(f"Error saving outputs: {e}")


def main():
    """Main function for command-line usage"""
    print("===== Enhanced Agentic Interview Preparation System =====")
    print("This system will:")
    print("1. Scrape and analyze the job description")
    print("2. Analyze your resume against the job")
    print("3. Generate a comprehensive 10+ page preparation report")
    print()

    job_url = input("Enter the Job Posting URL: ").strip()
    resume_file = input("Enter resume filename (from data/resumes/): ").strip()

    if not job_url or not resume_file:
        print("Job URL and resume file are required. Exiting...")
        return

    print(f"\nProcessing job URL: {job_url}")
    print(f"Analyzing resume: {resume_file}")
    print("This may take a few minutes...\n")

    result = generate_comprehensive_report(job_url, resume_file)

    if result.get("success"):
        print("✅ Comprehensive report generated successfully!")
        print(f"📄 HTML Report: data/reports/{resume_file}_comprehensive_report.html")
        print(
            f"📊 Analysis Data: data/reports/{resume_file}_comprehensive_analysis.json"
        )
        print(f"💼 Job Analysis: data/job_descriptions/enhanced_output.json")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
