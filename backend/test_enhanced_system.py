#!/usr/bin/env python3
"""
Test script for the Enhanced Agentic Interview Preparation System
"""

import os
import sys
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))


def test_enhanced_system():
    """Test the enhanced system with sample data"""
    print("🧪 Testing Enhanced Agentic Interview Preparation System")
    print("=" * 60)

    try:
        # Import the enhanced agent
        from app.agents.enhanced_comprehensive_agent import (
            generate_comprehensive_report,
        )

        # Test with sample data
        job_url = "https://example.com/job-posting"  # Replace with actual job URL
        resume_file = "swarnalatha.pdf"  # Use existing resume

        print(f"📋 Job URL: {job_url}")
        print(f"📄 Resume: {resume_file}")
        print("\n🚀 Starting comprehensive analysis...")

        # Generate comprehensive report
        result = generate_comprehensive_report(job_url, resume_file)

        if result.get("success"):
            print("✅ Test completed successfully!")
            print(f"📊 Job Analysis Keys: {list(result['job_analysis'].keys())}")
            print(f"📈 Resume Analysis Keys: {list(result['resume_analysis'].keys())}")
            print(f"📄 HTML Report Length: {len(result['html_report'])} characters")
        else:
            print(f"❌ Test failed: {result.get('error')}")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root directory")
    except Exception as e:
        print(f"❌ Test error: {e}")


def test_individual_components():
    """Test individual components"""
    print("\n🔧 Testing Individual Components")
    print("=" * 40)

    try:
        # Test job scraping
        from app.core.utils import scrape_job_description

        print("✅ Job scraping utility imported successfully")

        # Test resume reading
        from app.core.utils_agent2 import read_resume

        print("✅ Resume reading utility imported successfully")

        # Test OpenAI client
        from app.agents.enhanced_comprehensive_agent import client

        print("✅ OpenAI client initialized successfully")

        print("\n🎯 All components ready!")

    except Exception as e:
        print(f"❌ Component test failed: {e}")


if __name__ == "__main__":
    test_individual_components()
    print("\n" + "=" * 60)
    print("To run the full test, provide a valid job URL and ensure:")
    print("1. OpenAI API key is set in environment")
    print("2. Resume file exists in data/resumes/")
    print("3. All dependencies are installed")
    print("=" * 60)
