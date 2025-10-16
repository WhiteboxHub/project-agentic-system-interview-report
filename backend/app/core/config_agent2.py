# project-agentic-system-interview-report/backend/app/core/config_agent2.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Base directories
# Set backend root as base directory (one level up from 'app')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RESUME_DIR = os.path.join(BASE_DIR, "data/resumes")
JOB_DESC_DIR = os.path.join(BASE_DIR, "data/job_descriptions")
OUTPUT_DIR = os.path.join(BASE_DIR, "data/reports")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
