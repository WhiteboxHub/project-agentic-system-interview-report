#!/usr/bin/env python3
"""
Script to regenerate the HTML report with current datetime, credits, and copyright
"""

import json
from jinja2 import Template
from datetime import datetime

def regenerate_report():
    try:
        # Load the existing analysis data
        with open('data/reports/swarnalatha.pdf_comprehensive_analysis.json', 'r') as f:
            resume_analysis = json.load(f)

        with open('data/job_descriptions/enhanced_output.json', 'r') as f:
            job_analysis = json.load(f)

        # Load the template
        template_path = 'app/templates/report_template.html'
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Create Jinja2 template and render
        template = Template(template_content)
        
        # Get current datetime
        current_datetime = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        html_content = template.render(
            job=job_analysis, 
            resume=resume_analysis, 
            current_datetime=current_datetime
        )

        # Save the updated report
        output_path = 'data/reports/swarnalatha.pdf_comprehensive_report.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print('✅ HTML report regenerated successfully!')
        print(f'📁 Report saved to: {output_path}')
        print(f'📅 Generated on: {current_datetime}')
        print('👨‍💻 Credits: Hemant  , Jafar and Karimulla')
        print('©️ Copyright: 2025 Enhanced Agentic Interview Preparation System')
        print('-----------------------------9089968mygjghhhhhhhhhem')

    except FileNotFoundError as e:
        print(f'❌ Error: {e}')
        print('💡 Make sure the analysis files exist. Run the comprehensive agent first.')
    except Exception as e:
        print(f'❌ Error: {e}') 

if __name__ == "__main__":
    regenerate_report()
