# 🤖 Agentic Interview Preparation System

An AI-powered interview preparation system that uses multiple intelligent agents to analyze job descriptions and resumes, generating comprehensive 10+ page interview preparation reports.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

- **🔍 Enhanced Job Scraping**: Intelligent web scraping with better text extraction
- **📊 Comprehensive Analysis**: AI-powered job and resume analysis with detailed insights
- **📄 Professional Reports**: Beautiful 10+ page HTML reports with actionable guidance
- **🎯 Personalized Preparation**: Customized interview strategies and talking points
- **❓ Question Banks**: 50+ interview questions per category (technical, behavioral, company-specific)
- **🔑 Keywords & Phrases**: Industry-specific terms and technical keywords to use
- **⚠️ Gap Analysis**: Identifies missing skills and areas for improvement
- **🎤 Introduction Strategies**: Personalized elevator pitches and detailed introductions

## 🏗️ Architecture

The system consists of three main agents:

1. **Agent 1**: Job Description Analyzer - Scrapes and structures job postings
2. **Agent 2**: Resume Analysis Agent - Compares resumes against job descriptions
3. **Enhanced Comprehensive Agent**: Complete workflow combining both agents

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Internet connection for job scraping

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/WhiteboxHub/project-agentic-system-interview-report.git
cd project-agentic-system-interview-report
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv myvenv

# Activate virtual environment
# On macOS/Linux:
source myvenv/bin/activate

# On Windows:
# myvenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Set Environment Variables

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Or create a .env file in the backend directory
echo "OPENAI_API_KEY=your-openai-api-key-here" > backend/.env
```

### 5. Prepare Resume File

Place your resume (PDF or DOCX) in the `backend/data/resumes/` directory:

```bash
# Example: Copy your resume
cp your-resume.pdf backend/data/resumes/
```

### 6. Run the System

**Important**: Make sure you're in the **project root directory** before running the command:

```bash
# Ensure you're in the project root directory
pwd
# Should show: /path/to/project-agentic-system-interview-report

# Run the enhanced comprehensive agent
python3 -m backend.app.agents.enhanced_comprehensive_agent
```

## 📖 Usage Guide

### Complete Workflow (Recommended)

The enhanced comprehensive agent provides the full workflow:

```bash
python3 -m backend.app.agents.enhanced_comprehensive_agent
```

**Input prompts:**

1. Enter the Job Posting URL (e.g., LinkedIn, Indeed, company website)
2. Enter resume filename (e.g., `swarnalatha.pdf`)

**Output files:**

- `backend/data/job_descriptions/enhanced_output.json` - Job analysis
- `backend/data/reports/{resume_name}_comprehensive_analysis.json` - Resume analysis
- `backend/data/reports/{resume_name}_comprehensive_report.html` - HTML report

### Individual Agents

You can also run individual agents:

```bash
# Agent 1: Job Analysis only
python3 -m backend.app.agents.agent1_job_analysis

# Agent 2: Resume Analysis only
python3 -m backend.app.agents.agent2_question_retrieval
```

## 📊 Sample Output

### Job Analysis Features

- **Basic Information**: Job title, company, location, salary range
- **Technical Requirements**: Required skills, tools, technologies
- **Role Details**: Responsibilities, team structure, growth opportunities
- **Company Information**: Culture, values, benefits
- **Interview Insights**: Likely topics, assessment areas

### Resume Analysis Features

- **Executive Summary**: Overall match percentage (e.g., 85%)
- **Skills Analysis**: Match/partial/missing skill assessments
- **Personalized Introduction**: 30-second elevator pitch, 2-minute detailed intro
- **Technical Preparation**: Skills to brush up on, coding challenges
- **Interview Questions**: 50+ questions per category
- **Keywords & Phrases**: Technical terms and industry-specific language
- **Success Strategies**: Interview day preparation, body language tips

## 🗂️ Project Structure

```
project-agentic-system-interview-report/
├── backend/                           # Main application code
│   ├── app/                          # Core application modules
│   │   ├── agents/                   # AI agents
│   │   │   ├── agent1_job_analysis.py
│   │   │   ├── agent2_question_retrieval.py
│   │   │   └── enhanced_comprehensive_agent.py
│   │   ├── core/                     # Core utilities and configuration
│   │   │   ├── config.py
│   │   │   ├── config_agent2.py
│   │   │   ├── utils.py
│   │   │   ├── utils_agent2.py
│   │   │   ├── logging.py
│   │   │   └── logging_agent2.py
│   │   ├── db/                       # Database models
│   │   ├── templates/                # HTML report templates
│   │   │   └── report_template.html
│   │   └── main.py                   # FastAPI application
│   ├── data/                         # Data storage
│   │   ├── job_descriptions/         # Processed job data
│   │   ├── reports/                  # Generated analysis reports
│   │   └── resumes/                  # Candidate resume files
│   ├── logs/                         # Application logs
│   ├── tests/                        # Test files
│   ├── requirements.txt              # Python dependencies
│   └── Dockerfile                    # Container configuration
├── docker-compose.yml                # Multi-container orchestration
├── myvenv/                          # Python virtual environment
└── README.md                        # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

### Dependencies

Key dependencies include:

- `fastapi` - Web framework
- `openai` - OpenAI API client
- `beautifulsoup4` - Web scraping
- `docling` - Document processing
- `pdfplumber` - PDF text extraction
- `python-docx` - DOCX file processing
- `jinja2` - HTML template engine

## 🐳 Docker Support

The project includes Docker configuration for containerized deployment:

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📝 Example Workflow

1. **Prepare**: Place resume in `backend/data/resumes/`
2. **Run**: Execute the enhanced comprehensive agent
3. **Input**: Provide job URL and resume filename
4. **Wait**: System processes (2-3 minutes)
5. **Review**: Check generated HTML report

### Sample Job URLs

- LinkedIn: `https://www.linkedin.com/jobs/view/...`
- Indeed: `https://www.indeed.com/viewjob?jk=...`
- Company websites: `https://company.com/careers/job/...`

## 🎯 Use Cases

- **Job Seekers**: Comprehensive interview preparation
- **Career Coaches**: Client preparation assistance
- **HR Teams**: Candidate assessment and preparation
- **Recruiters**: Interview guidance for candidates
- **Students**: Career preparation and skill gap analysis

## 🔍 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure virtual environment is activated
2. **OpenAI API Error**: Check API key and credits
3. **Job Scraping Failed**: Verify URL is accessible
4. **Resume Not Found**: Check file exists in `backend/data/resumes/`

### Debug Mode

Enable detailed logging by checking log files in `backend/logs/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini API
- BeautifulSoup for web scraping capabilities
- Docling for document processing
- The open-source community for various Python libraries

## 📞 Support

For support, email support@whiteboxhub.com or create an issue in this repository.

## 🔗 Links

- [GitHub Repository](https://github.com/WhiteboxHub/project-agentic-system-interview-report)
- [Documentation](https://github.com/WhiteboxHub/project-agentic-system-interview-report/wiki)
- [Issues](https://github.com/WhiteboxHub/project-agentic-system-interview-report/issues)

---

**Made with ❤️ by WhiteboxHub**
