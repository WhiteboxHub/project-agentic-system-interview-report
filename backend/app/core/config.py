# project-agentic-system-interview-report/backend/app/core/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "job_descriptions")

os.makedirs(OUTPUT_DIR, exist_ok=True)
