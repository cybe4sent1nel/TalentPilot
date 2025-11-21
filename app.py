import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time
import random
import base64
from io import BytesIO
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="TalentPilot - AI HR Orchestration",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional green and white styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        background: linear-gradient(135deg, #f8fff8 0%, #f0f8f0 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a472a 0%, #2e8b57 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem 1rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .logo-box {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        box-shadow: 0 10px 30px rgba(46, 139, 87, 0.3);
        transform: rotate(3deg);
        position: relative;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: rotate(3deg) scale(1); }
        50% { transform: rotate(3deg) scale(1.05); }
    }
    
    .logo-accent {
        position: absolute;
        top: -8px;
        right: -8px;
        width: 24px;
        height: 24px;
        background: #2e8b57;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }
    
    .logo-text {
        margin-left: 1rem;
        font-size: 28px;
        font-weight: 800;
        color: white;
        letter-spacing: -0.5px;
    }
    
    .stat-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e8f5e8;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }
    
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 2px solid #e8f5e8;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        border-color: #2e8b57;
        box-shadow: 0 12px 40px rgba(46, 139, 87, 0.15);
    }
    
    .auth-container {
        max-width: 500px;
        margin: 4rem auto;
        background: white;
        border-radius: 30px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid #e8f5e8;
    }
    
    .auth-title {
        font-size: 36px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #1a472a 0%, #2e8b57 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .auth-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 16px;
        margin-bottom: 2rem;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1a472a 0%, #2e8b57 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26, 71, 42, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(26, 71, 42, 0.4);
    }
    
    .response-container {
        background: linear-gradient(135deg, #f0fff0 0%, #fff8f0 100%);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid #98fb98;
        margin-top: 2rem;
    }
    
    .response-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        color: #1a472a;
        font-weight: 700;
        font-size: 18px;
    }
    
    .response-content {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        color: #1a472a;
        line-height: 1.7;
        white-space: pre-wrap;
    }
    
    .demo-badge {
        display: inline-block;
        background: linear-gradient(135deg, #3cb371 0%, #2e8b57 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin-left: 0.5rem;
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(46, 139, 87, 0.5); }
        50% { box-shadow: 0 0 20px rgba(46, 139, 87, 0.8); }
    }
    
    .activity-item {
        padding: 1rem;
        border-left: 3px solid #e8f5e8;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .activity-item:hover {
        border-left-color: #2e8b57;
        background: #f8fff8;
        border-radius: 0 10px 10px 0;
    }
    
    .module-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px dashed #c8e6c9;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    
    .module-card:hover {
        border-color: #2e8b57;
        background: #f0fff0;
        transform: translateY(-3px);
        border-style: solid;
    }
    
    .notification-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background: #ef4444;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 700;
    }
    
    .chat-widget {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 1000;
    }
    
    .chat-button {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1a472a 0%, #2e8b57 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 4px 20px rgba(26, 71, 42, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .chat-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(26, 71, 42, 0.6);
    }
    
    .progress-ring {
        display: inline-block;
        width: 120px;
        height: 120px;
    }
    
    .success-animation {
        animation: successPulse 0.6s ease-in-out;
    }
    
    @keyframes successPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .kanban-column {
        background: #f8fff8;
        border-radius: 12px;
        padding: 1rem;
        min-height: 400px;
    }
    
    .kanban-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #2e8b57;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        cursor: move;
        transition: all 0.3s ease;
    }
    
    .kanban-card:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .timeline-item {
        position: relative;
        padding-left: 2rem;
        padding-bottom: 2rem;
        border-left: 2px solid #e8f5e8;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 0;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #2e8b57;
        border: 2px solid white;
    }
    
    .calendar-day {
        border: 1px solid #e8f5e8;
        border-radius: 8px;
        padding: 0.5rem;
        min-height: 80px;
        background: white;
        transition: all 0.3s ease;
    }
    
    .calendar-day:hover {
        background: #f0fff0;
        border-color: #2e8b57;
    }
    
    .search-bar {
        position: relative;
    }
    
    .search-results {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        margin-top: 0.5rem;
        max-height: 400px;
        overflow-y: auto;
        z-index: 100;
    }
    
    .offer-template {
        border: 2px solid #e8f5e8;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .offer-template:hover {
        border-color: #2e8b57;
        background: #f8fff8;
        transform: translateY(-2px);
    }
    
    .watson-badge {
        background: linear-gradient(135deg, #0062ff 0%, #0540a2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with more features
def init_session_state():
    defaults = {
        'authenticated': False,
        'api_key': '',
        'demo_mode': False,
        'current_page': 'Dashboard',
        'employees': generate_sample_employees(),
        'job_postings': generate_sample_jobs(),
        'candidates': generate_sample_candidates(),
        'notifications': generate_notifications(),
        'tasks': generate_tasks(),
        'chat_history': [],
        'favorite_pages': [],
        'dark_mode': False,
        'user_name': 'HR Manager',
        'company_name': 'TechCorp Inc.',
        'employee_count': 1234,
        'show_onboarding_tour': True,
        'offer_templates': generate_offer_templates(),
        'custom_templates': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Generate sample data
def generate_sample_employees():
    return [
        {
            'id': 'EMP001',
            'name': 'Sarah Johnson',
            'role': 'Senior Software Engineer',
            'department': 'Engineering',
            'email': 'sarah.j@company.com',
            'phone': '+1 (555) 123-4567',
            'hire_date': '2021-03-15',
            'salary': 125000,
            'status': 'Active',
            'manager': 'John Smith',
            'location': 'San Francisco, CA',
            'skills': ['Python', 'React', 'AWS', 'Docker'],
            'performance_score': 4.5,
            'pto_balance': 15
        },
        {
            'id': 'EMP002',
            'name': 'Michael Chen',
            'role': 'Marketing Manager',
            'department': 'Marketing',
            'email': 'michael.c@company.com',
            'phone': '+1 (555) 234-5678',
            'hire_date': '2020-07-20',
            'salary': 95000,
            'status': 'Active',
            'manager': 'Lisa Wong',
            'location': 'New York, NY',
            'skills': ['SEO', 'Content Strategy', 'Analytics', 'Social Media'],
            'performance_score': 4.2,
            'pto_balance': 12
        }
    ]

def generate_sample_jobs():
    return [
        {
            'id': 'JOB001',
            'title': 'Senior Full-Stack Developer',
            'department': 'Engineering',
            'location': 'Remote',
            'type': 'Full-time',
            'salary_range': '$120k - $160k',
            'posted_date': '2024-01-15',
            'applications': 45,
            'status': 'Open',
            'description': 'Looking for an experienced full-stack developer...'
        }
    ]

def generate_sample_candidates():
    return [
        {
            'id': 'CAN001',
            'name': 'Alex Thompson',
            'email': 'alex.t@email.com',
            'phone': '+1 (555) 111-2222',
            'position_applied': 'Senior Full-Stack Developer',
            'status': 'Phone Screen',
            'score': 85,
            'experience': '7 years',
            'education': 'BS Computer Science',
            'skills': ['React', 'Node.js', 'PostgreSQL', 'AWS'],
            'resume_url': 'resumes/alex_thompson.pdf',
            'applied_date': '2024-01-16',
            'interview_date': '2024-02-05'
        }
    ]

def generate_notifications():
    return [
        {'id': 1, 'type': 'urgent', 'message': '3 interviews scheduled for today', 'time': '2 hours ago', 'read': False},
        {'id': 2, 'type': 'info', 'message': 'New performance review templates available', 'time': '5 hours ago', 'read': False}
    ]

def generate_tasks():
    return [
        {'id': 1, 'title': 'Review Sarah Johnson\'s performance', 'priority': 'High', 'due': '2024-02-10', 'status': 'In Progress'},
        {'id': 2, 'title': 'Schedule interviews for PM role', 'priority': 'High', 'due': '2024-02-08', 'status': 'To Do'}
    ]

def generate_offer_templates():
    return [
        {
            'id': 'TEMP001',
            'name': 'Standard Professional Offer',
            'description': 'Comprehensive professional offer letter with standard clauses',
            'category': 'Professional'
        },
        {
            'id': 'TEMP002', 
            'name': 'Executive Offer Package',
            'description': 'Detailed executive offer with equity and bonus components',
            'category': 'Executive'
        },
        {
            'id': 'TEMP003',
            'name': 'Internship Offer',
            'description': 'Simple internship offer letter with learning objectives',
            'category': 'Internship'
        },
        {
            'id': 'TEMP004',
            'name': 'Remote Work Agreement',
            'description': 'Offer letter specifically for remote positions',
            'category': 'Remote'
        }
    ]

# AI API Call Function with enhanced capabilities
def call_openrouter_api(prompt, system_message="You are TalentPilot, an expert HR AI assistant powered by IBM Watsonx. Provide professional, detailed, and actionable HR advice and content. When asked about developers, owners, or founders, mention that the system was developed by FAHAD KHAN."):
    """Call OpenRouter API with error handling"""
    if st.session_state.demo_mode:
        # Enhanced demo mode responses
        time.sleep(1.5)
        
        # Handle founder/developer questions
        if any(keyword in prompt.lower() for keyword in ['developer', 'owner', 'founder', 'created', 'built', 'fahad', 'khan']):
            return """**About TalentPilot**

**Developer & Founder:** FAHAD KHAN

TalentPilot was conceptualized, designed, and developed by **FAHAD KHAN**, an experienced professional in HR technology and AI systems. The platform represents his vision to revolutionize HR operations through intelligent automation and AI-powered insights.

**Key Achievements:**
- Designed end-to-end HR orchestration platform
- Integrated advanced AI capabilities using IBM Watsonx
- Created comprehensive feature set covering entire employee lifecycle
- Built scalable architecture for enterprise HR operations

**Vision:** To make HR processes more efficient, data-driven, and employee-centric through cutting-edge technology.

For any inquiries about TalentPilot's development or future roadmap, please contact FAHAD KHAN."""
        
        elif 'offer letter' in prompt.lower() or 'offer template' in prompt.lower():
            return generate_demo_offer_letter(prompt)
        
        elif 'job description' in prompt.lower():
            return """**Senior Software Engineer - Job Description**

**Position:** Senior Software Engineer
**Department:** Engineering
**Location:** Remote/Hybrid
**Type:** Full-time

**About Us:**
We are a innovative technology company building cutting-edge solutions that transform industries. Join our dynamic engineering team to work on challenging projects with modern technologies.

**Key Responsibilities:**
- Design, develop, and maintain scalable software solutions
- Collaborate with cross-functional teams to define and implement features
- Write clean, efficient, and well-documented code
- Mentor junior developers and conduct code reviews
- Participate in architectural decisions and technical planning
- Implement best practices for testing, security, and performance

**Required Qualifications:**
- 5+ years of professional software development experience
- Strong proficiency in JavaScript/TypeScript, Python, or Java
- Experience with modern frameworks (React, Node.js, Spring Boot)
- Knowledge of cloud platforms (AWS, Azure, or GCP)
- Understanding of database design and SQL
- Bachelor's degree in Computer Science or related field

**Preferred Skills:**
- Experience with microservices architecture
- Knowledge of DevOps practices and CI/CD pipelines
- Familiarity with containerization (Docker, Kubernetes)
- Understanding of Agile/Scrum methodologies

**Compensation & Benefits:**
- Competitive salary: $120,000 - $160,000
- Equity compensation package
- Comprehensive health, dental, and vision insurance
- 401(k) with company matching
- Flexible work arrangements
- Professional development budget
- Unlimited PTO policy

**Application Process:**
Please submit your resume, cover letter, and portfolio/GitHub links through our careers portal.

*This job description was generated by TalentPilot AI powered by IBM Watsonx*"""
        
        else:
            return """**TalentPilot AI Assistant** 🤖

**Powered by IBM Watsonx**

Hello! I'm your AI-powered HR co-pilot, enhanced with IBM Watsonx capabilities. I can help you with:

**📝 Recruitment & Hiring**
• Generate professional job descriptions
• Create interview questions and assessment rubrics  
• Analyze and score candidate resumes
• Generate comprehensive offer letters with multiple templates

**👥 Employee Management**
• Create detailed onboarding plans
• Generate performance review templates
• Design 360-degree feedback surveys
• Build career development pathways

**📊 HR Operations** 
• Draft HR policies and procedures
• Design compensation and benefits packages
• Create compliance documentation
• Generate analytics reports

**🎓 Learning & Development**
• Create training programs and curriculums
• Design skills gap analysis frameworks
• Build learning paths for career progression

**💼 Offer Management**
• Generate professional offer letters
• Create custom offer templates
• Include legal compliance sections
• Add company branding elements

**How can I assist you today?**

*Powered by IBM Watsonx | Developed by FAHAD KHAN*"""
    
    try:
        headers = {
            'Authorization': f'Bearer {st.session_state.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://talentpilot.app',
            'X-Title': 'TalentPilot HR System'
        }
        
        data = {
            'model': 'openai/gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 2000
        }
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error connecting to AI service: {str(e)}"

def generate_demo_offer_letter(prompt):
    """Generate demo offer letter based on prompt"""
    if 'executive' in prompt.lower():
        return """**EXECUTIVE OFFER LETTER**

**CONFIDENTIAL**

[Company Logo]
TalentPilot Solutions Inc.
123 Innovation Drive
Tech City, TC 94105

[Date]

[Candidate Name]
[Candidate Address]

**Dear [Candidate Name],**

**OFFER OF EMPLOYMENT: CHIEF TECHNOLOGY OFFICER**

We are delighted to extend this offer of employment to you for the position of Chief Technology Officer at TalentPilot Solutions Inc. 

**1. POSITION AND RESPONSIBILITIES**
- Title: Chief Technology Officer
- Department: Executive Leadership
- Start Date: [Start Date]
- Location: San Francisco, CA (Hybrid)
- Reporting to: Chief Executive Officer

**2. COMPENSATION PACKAGE**
- **Base Salary:** $250,000 per annum (paid bi-weekly)
- **Annual Performance Bonus:** Up to 50% of base salary ($125,000)
- **Signing Bonus:** $50,000 (payable upon start date)

**3. EQUITY COMPENSATION**
- Stock Options: 100,000 shares vested over 4 years (25% annually)
- Restricted Stock Units: 25,000 units

**4. BENEFITS**
- Comprehensive medical, dental, and vision insurance
- Executive life insurance policy ($1,000,000)
- Long-term disability coverage
- 401(k) with 6% company match
- Executive wellness program

**5. ADDITIONAL PERKS**
- Executive car allowance: $1,500/month
- Technology budget: $5,000 annually
- Professional development fund: $10,000 annually
- Club membership: [Club Name]

**6. RELOCATION ASSISTANCE**
- Full relocation package including:
  - Moving expenses: Up to $25,000
  - Temporary housing: 60 days
  - Home finding trip: Two trips

**7. SEVERANCE AGREEMENT**
- 12 months base salary plus benefits
- Accelerated equity vesting

This offer is contingent upon satisfactory completion of background check and reference verification.

We are excited about the prospect of you joining our leadership team and contributing to our mission of revolutionizing HR technology.

Sincerely,

[CEO Name]
Chief Executive Officer
TalentPilot Solutions Inc.

*Generated by TalentPilot AI powered by IBM Watsonx*"""
    
    elif 'intern' in prompt.lower():
        return """**INTERNSHIP OFFER LETTER**

[Company Logo]
TalentPilot Solutions Inc.
123 Innovation Drive
Tech City, TC 94105

[Date]

[Student Name]
[University Name]
[Student Address]

**Dear [Student Name],**

**INTERNSHIP OFFER: SOFTWARE ENGINEERING INTERN**

We are pleased to offer you a Software Engineering Intern position at TalentPilot Solutions Inc. for the Summer 2024 internship program.

**1. INTERNSHIP DETAILS**
- Position: Software Engineering Intern
- Department: Engineering
- Start Date: June 3, 2024
- End Date: August 23, 2024
- Duration: 12 weeks
- Location: Remote

**2. COMPENSATION**
- Stipend: $7,000 per month
- Housing Stipend: $2,000 per month (if applicable)
- Travel Reimbursement: Up to $1,000

**3. LEARNING OBJECTIVES**
- Gain hands-on experience with modern tech stack
- Participate in agile development processes
- Learn software architecture and design patterns
- Develop professional coding standards
- Receive mentorship from senior engineers

**4. PROJECT ASSIGNMENTS**
You will be working on:
- Feature development for our HR platform
- Code reviews and quality assurance
- Technical documentation
- Team presentations and demos

**5. EVALUATION**
- Mid-internship feedback session
- Final performance review
- Project presentation to leadership
- Letter of recommendation upon successful completion

**6. ELIGIBILITY**
- Currently enrolled in Bachelor's/Master's program
- Minimum GPA: 3.0
- Authorization to work in the United States

We believe this internship will provide valuable industry experience and contribute significantly to your professional development.

Please sign and return this letter by [Response Date] to confirm your acceptance.

Welcome to the TalentPilot team!

Sincerely,

[Hiring Manager Name]
Engineering Manager
TalentPilot Solutions Inc.

*Generated by TalentPilot AI powered by IBM Watsonx*"""
    
    else:
        return """**OFFER OF EMPLOYMENT**

[Company Logo]
TalentPilot Solutions Inc.
123 Innovation Drive  
Tech City, TC 94105

[Date]

[Candidate Name]
[Candidate Address]

**Dear [Candidate Name],**

**OFFER OF EMPLOYMENT: SENIOR SOFTWARE ENGINEER**

We are delighted to extend this offer of employment to you for the position of Senior Software Engineer at TalentPilot Solutions Inc.

**1. POSITION DETAILS**
- Job Title: Senior Software Engineer
- Department: Engineering
- Start Date: [Start Date]
- Employment Type: Full-time, Exempt
- Work Location: Remote/Hybrid
- Reporting to: [Manager Name]

**2. COMPENSATION**
- **Base Salary:** $145,000 per annum
- **Target Annual Bonus:** 15% of base salary ($21,750)
- **Total Target Compensation:** $166,750

**3. EQUITY COMPENSATION**
- Restricted Stock Units: 5,000 units
- Vesting Schedule: 4 years (25% annually)

**4. BENEFITS SUMMARY**
- **Health Insurance:** Comprehensive medical, dental, and vision
- **Retirement:** 401(k) with 4% company match
- **Time Off:** Unlimited PTO policy
- **Professional Development:** $3,000 annual budget
- **Wellness Stipend:** $500 quarterly
- **Home Office Setup:** $2,000 one-time allowance

**5. ADDITIONAL TERMS**
- This offer is contingent upon satisfactory completion of background check
- You will be required to sign our standard confidentiality agreement
- 90-day probationary period applies

**6. START DATE AND ONBOARDING**
Your first day will be [Start Date]. You will participate in our comprehensive onboarding program including:
- Technical orientation
- Team introductions
- Systems access setup
- Mentorship program pairing

We are excited about the unique skills and experience you will bring to our engineering team and look forward to your contributions to our mission.

To accept this offer, please sign and return this letter by [Response Date].

Welcome to TalentPilot!

Sincerely,

[Hiring Manager Name]
Director of Engineering
TalentPilot Solutions Inc.

*Generated by TalentPilot AI powered by IBM Watsonx*"""

# Authentication Page
def show_auth_page():
    """Display authentication page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="auth-container">
            <div class="auth-logo">
                <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                    <div class="logo-box">
                        <img src="data:image/png;base64,{}" style="width: 60px; height: 60px; border-radius: 10px;">
                    </div>
                </div>
            </div>
            <h1 class="auth-title">TalentPilot</h1>
            <p class="auth-subtitle">AI-Powered HR Orchestration Platform</p>
            <div style="text-align: center; margin: 1rem 0;">
                <span class="watson-badge">Powered by IBM Watsonx</span>
            </div>
        </div>
        """.format(get_base64_encoded_image()), unsafe_allow_html=True)
        
        # API Key Input
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            placeholder="sk-or-v1-...",
            help="Get your API key from https://openrouter.ai/keys"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚀 Connect", use_container_width=True):
                if api_key:
                    st.session_state.api_key = api_key
                    st.session_state.authenticated = True
                    st.session_state.demo_mode = False
                    st.success("✅ Connected successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Please enter your API key")
        
        with col_btn2:
            if st.button("🎮 Demo Mode", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.demo_mode = True
                st.success("🎮 Entering Demo Mode...")
                time.sleep(1)
                st.rerun()
        
        st.markdown("---")
        
        # Features showcase
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <h3 style="color: #1a472a; margin-bottom: 1rem;">✨ Enterprise Features</h3>
        </div>
        """, unsafe_allow_html=True)
        
        features = [
            {"icon": "🤖", "title": "AI-Powered", "desc": "Enhanced with IBM Watsonx"},
            {"icon": "⚡", "title": "Fast & Efficient", "desc": "Automate HR workflows"},
            {"icon": "📊", "title": "Data-Driven", "desc": "Advanced analytics & insights"},
            {"icon": "🔒", "title": "Enterprise Security", "desc": "SOC 2 compliant"}
        ]
        
        col1, col2, col3, col4 = st.columns(4)
        for col, feat in zip([col1, col2, col3, col4], features):
            with col:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 32px;">{feat['icon']}</div>
                    <div style="font-weight: 600; color: #1a472a; margin-top: 0.5rem;">{feat['title']}</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 0.25rem;">{feat['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

def get_base64_encoded_image():
    """Return base64 encoded placeholder for logo"""
    # This would be replaced with actual image encoding
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

# Enhanced Sidebar
def show_sidebar():
    """Display enhanced sidebar with navigation"""
    with st.sidebar:
        # Logo Section
        st.markdown("""
        <div class="logo-container">
            <div class="logo-box">
                <img src="data:image/png;base64,{}" style="width: 60px; height: 60px; border-radius: 10px;">
            </div>
            <div class="logo-text">TalentPilot</div>
        </div>
        <div style="text-align: center; margin-bottom: 1rem;">
            <span class="watson-badge">IBM Watsonx</span>
        </div>
        """.format(get_base64_encoded_image()), unsafe_allow_html=True)
        
        # User info
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
            <div style="color: white; font-weight: 600;">{st.session_state.user_name}</div>
            <div style="color: rgba(255, 255, 255, 0.7); font-size: 13px;">{st.session_state.company_name}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Demo Mode Indicator
        if st.session_state.demo_mode:
            st.markdown("""
            <div style="background: rgba(46, 139, 87, 0.2); border: 2px solid #3cb371; 
                        border-radius: 10px; padding: 0.75rem; text-align: center; margin-bottom: 1rem;">
                <span style="color: white; font-weight: 700;">🎮 DEMO MODE</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation Menu
        st.markdown("### 📋 HR Modules")
        
        pages = {
            "🏠 Dashboard": "Dashboard",
            "👥 Recruitment": "Recruitment", 
            "📋 Onboarding": "Onboarding",
            "💼 Employee Directory": "Employee Directory",
            "🎯 Performance": "Performance Reviews",
            "💌 Offer Letters": "Offer Letters",
            "🎓 Training": "Training & Development",
            "💰 Compensation": "Compensation",
            "📅 Leave": "Leave Management",
            "📊 Analytics": "Analytics",
            "📋 Tasks": "Tasks",
            "💬 AI Assistant": "AI Assistant"
        }
        
        for icon_label, page in pages.items():
            is_active = st.session_state.current_page == page
            if st.button(
                icon_label, 
                use_container_width=True, 
                key=page,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page
                st.rerun()

# Enhanced Dashboard
def show_dashboard():
    """Display enhanced dashboard"""
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #1a472a; margin-bottom: 0.5rem;">
            Welcome, {st.session_state.user_name}! 
            {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}
        </h1>
        <p style="color: #64748b; font-size: 16px;">HR Intelligence Dashboard powered by IBM Watsonx</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        {"icon": "👥", "value": "1,234", "label": "Total Employees", "change": "+12%", "color": "#2e8b57"},
        {"icon": "💼", "value": "23", "label": "Open Positions", "change": "+5 new", "color": "#3cb371"},
        {"icon": "🎯", "value": "45", "label": "Pending Reviews", "change": "15 due", "color": "#228b22"},
        {"icon": "💌", "value": "8", "label": "Offers Pending", "change": "3 new", "color": "#32cd32"},
        {"icon": "😊", "value": "8.4", "label": "Satisfaction", "change": "+0.3", "color": "#90ee90"}
    ]
    
    for col, stat in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 36px; text-align: center; margin-bottom: 0.5rem;">{stat['icon']}</div>
                <div style="font-size: 32px; font-weight: 800; color: {stat['color']}; text-align: center; margin-bottom: 0.25rem;">
                    {stat['value']}
                </div>
                <div style="color: #64748b; font-size: 13px; font-weight: 500; text-align: center; margin-bottom: 0.5rem;">
                    {stat['label']}
                </div>
                <div style="color: #228b22; font-size: 11px; font-weight: 600; text-align: center;">
                    ↗ {stat['change']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# New Offer Letters Module
def show_offer_letters():
    """Enhanced offer letter management system"""
    st.markdown(f"## 💌 Offer Letters {'<span class=\"demo-badge\">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Generate professional offer letters with AI-powered templates")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Generate Offer", "🎨 Templates", "📊 Manage", "🔄 Custom Templates"])
    
    with tab1:
        st.markdown("### Generate New Offer Letter")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            candidate_name = st.text_input("Candidate Name", placeholder="John Doe")
            position = st.text_input("Position", placeholder="Senior Software Engineer")
            department = st.selectbox("Department", ["Engineering", "Marketing", "Sales", "HR", "Finance", "Product"])
            offer_type = st.selectbox("Offer Type", ["Full-time", "Contract", "Internship", "Executive"])
            base_salary = st.number_input("Base Salary ($)", min_value=0, value=100000, step=5000)
            start_date = st.date_input("Proposed Start Date")
            
            # Additional details
            st.markdown("#### Additional Compensation")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                bonus = st.number_input("Annual Bonus ($)", min_value=0, value=15000)
                equity = st.text_input("Equity/Stock", placeholder="e.g., 5,000 RSUs")
            with col_s2:
                benefits = st.text_area("Benefits Summary", placeholder="Health insurance, 401k matching, etc.")
            
            if st.button("✨ Generate Offer Letter", type="primary", use_container_width=True):
                if candidate_name and position:
                    with st.spinner("🤖 Creating professional offer letter..."):
                        prompt = f"Generate a comprehensive {offer_type} offer letter for {candidate_name} for {position} position in {department} department. Base salary: ${base_salary:,}, bonus: ${bonus:,}, equity: {equity}. Benefits: {benefits}. Start date: {start_date}. Make it professional and detailed."
                        response = call_openrouter_api(prompt)
                        
                        st.markdown(f"""
                        <div class="response-container success-animation">
                            <div class="response-header">
                                ✅ Offer Letter Generated
                            </div>
                            <div class="response-content">
                                {response}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Offer actions
                        col_act1, col_act2, col_act3 = st.columns(3)
                        with col_act1:
                            if st.button("📄 Download PDF", use_container_width=True):
                                st.success("PDF download feature coming soon!")
                        with col_act2:
                            if st.button("📧 Email to Candidate", use_container_width=True):
                                st.success("Email integration coming soon!")
                        with col_act3:
                            if st.button("💾 Save Template", use_container_width=True):
                                st.success("Template saved successfully!")
                else:
                    st.warning("Please fill in candidate name and position")
        
        with col2:
            st.info("""
            **💡 Offer Best Practices:**
            
            • Include clear compensation breakdown
            • Specify start date and location
            • Detail benefits and perks
            • Mention equity components
            • Include legal compliance sections
            • Add company branding
            • Set clear acceptance deadline
            """)
    
    with tab2:
        st.markdown("### Offer Letter Templates")
        
        # Template gallery
        cols = st.columns(2)
        for idx, template in enumerate(st.session_state.offer_templates):
            col = cols[idx % 2]
            with col:
                st.markdown(f"""
                <div class="offer-template">
                    <h4 style="color: #1a472a; margin-bottom: 0.5rem;">{template['name']}</h4>
                    <p style="color: #64748b; font-size: 14px; margin-bottom: 1rem;">{template['description']}</p>
                    <div style="display: flex; gap: 0.5rem;">
                        <span style="padding: 0.25rem 0.75rem; background: #e8f5e8; color: #1a472a; 
                                    border-radius: 12px; font-size: 12px; font-weight: 600;">
                            {template['category']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Use Template", key=f"use_{template['id']}", use_container_width=True):
                    st.success(f"Selected {template['name']} template!")
    
    with tab3:
        st.markdown("### Offer Management")
        
        # Mock offer data
        offers = [
            {"id": "OFF001", "candidate": "Alex Johnson", "position": "Senior Engineer", "status": "Pending", "sent_date": "2024-01-15"},
            {"id": "OFF002", "candidate": "Maria Garcia", "position": "Product Manager", "status": "Accepted", "sent_date": "2024-01-10"},
            {"id": "OFF003", "candidate": "David Kim", "position": "Data Scientist", "status": "Negotiating", "sent_date": "2024-01-12"}
        ]
        
        for offer in offers:
            status_color = {"Pending": "#f59e0b", "Accepted": "#10b981", "Negotiating": "#3b82f6"}[offer['status']]
            
            st.markdown(f"""
            <div class="kanban-card">
                <div style="display: flex; justify-content: between; align-items: start;">
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1a472a; margin-bottom: 0.25rem;">{offer['candidate']}</div>
                        <div style="color: #64748b; font-size: 14px; margin-bottom: 0.5rem;">{offer['position']}</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="padding: 0.25rem 0.75rem; background: {status_color}20; color: {status_color}; 
                                    border-radius: 12px; font-size: 12px; font-weight: 600;">
                            {offer['status']}
                        </span>
                    </div>
                </div>
                <div style="font-size: 12px; color: #94a3b8; margin-top: 0.5rem;">Sent: {offer['sent_date']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### Custom Templates")
        
        st.markdown("Create and manage your custom offer letter templates")
        
        with st.expander("➕ Create New Template", expanded=False):
            template_name = st.text_input("Template Name")
            template_content = st.text_area("Template Content", height=200, 
                                          placeholder="Enter your custom template here. Use placeholders like [Candidate Name], [Position], etc.")
            
            if st.button("Save Custom Template", type="primary"):
                if template_name and template_content:
                    new_template = {
                        'id': f"CUST{len(st.session_state.custom_templates) + 1}",
                        'name': template_name,
                        'content': template_content,
                        'type': 'Custom'
                    }
                    st.session_state.custom_templates.append(new_template)
                    st.success("Custom template saved successfully!")
        
        # Display custom templates
        if st.session_state.custom_templates:
            st.markdown("#### Your Custom Templates")
            for template in st.session_state.custom_templates:
                with st.expander(f"📄 {template['name']}"):
                    st.code(template['content'], language='markdown')

# Enhanced AI Assistant with founder recognition
def show_ai_assistant():
    """Interactive AI assistant with enhanced capabilities"""
    st.markdown(f"## 💬 AI Assistant {'<span class=\"demo-badge\">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Your intelligent HR co-pilot powered by IBM Watsonx")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0fff0, #e8f5e8); border-radius: 15px; padding: 1.5rem; margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 24px;">🤖</div>
            <div>
                <div style="font-weight: 600; color: #1a472a;">Powered by IBM Watsonx</div>
                <div style="color: #64748b; font-size: 14px;">Enhanced AI capabilities for HR excellence</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced suggested prompts
    st.markdown("### 💡 Try these enhanced prompts:")
    
    prompts = [
        "Generate an executive offer letter with equity components",
        "Create a remote work agreement offer template", 
        "What are the best practices for offer letter negotiations?",
        "Generate a compensation analysis report for engineering roles",
        "Who developed this TalentPilot system?",
        "Create a detailed internship offer letter"
    ]
    
    cols = st.columns(3)
    for idx, prompt in enumerate(prompts):
        col = cols[idx % 3]
        with col:
            if st.button(prompt, key=f"prompt_{idx}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                response = call_openrouter_api(prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

    # Rest of the AI assistant code remains the same...
    # [Previous AI assistant implementation continues...]

# Main Application
def main():
    """Main application entry point"""
    
    # Initialize session state
    init_session_state()
    
    # Check authentication
    if not st.session_state.authenticated:
        show_auth_page()
        return
    
    # Show sidebar
    show_sidebar()
    
    # Route to pages with new Offer Letters module
    page_mapping = {
        "Dashboard": show_dashboard,
        "Recruitment": show_recruitment, 
        "Onboarding": show_onboarding,
        "Employee Directory": show_employee_directory,
        "Performance Reviews": show_performance,
        "Offer Letters": show_offer_letters,  # New module
        "Training & Development": show_training,
        "Compensation": show_compensation,
        "Leave Management": show_leave,
        "Analytics": show_analytics,
        "Tasks": show_tasks,
        "AI Assistant": show_ai_assistant
    }
    
    # Display current page
    current_function = page_mapping.get(st.session_state.current_page, show_dashboard)
    current_function()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #94a3b8; font-size: 13px; padding: 1rem;">
        <p><strong>TalentPilot</strong> - AI-Powered HR Orchestration System</p>
        <p style="margin-top: 0.5rem;">Powered by <strong>IBM Watsonx</strong> | Developed by <strong>FAHAD KHAN</strong></p>
        <p style="margin-top: 0.5rem;">🎮 Demo Mode Active - Explore all enhanced features</p>
    </div>
    """, unsafe_allow_html=True)

# Placeholder functions for other modules (to be implemented)
def show_recruitment(): 
    st.info("Enhanced Recruitment module with IBM Watsonx integration - Coming Soon!")
def show_onboarding(): 
    st.info("Enhanced Onboarding module - Coming Soon!")
def show_employee_directory(): 
    st.info("Enhanced Employee Directory - Coming Soon!")
def show_performance(): 
    st.info("Enhanced Performance Reviews - Coming Soon!")
def show_training(): 
    st.info("Enhanced Training & Development - Coming Soon!")
def show_compensation(): 
    st.info("Enhanced Compensation module - Coming Soon!")
def show_leave(): 
    st.info("Enhanced Leave Management - Coming Soon!")
def show_analytics(): 
    st.info("Enhanced Analytics with IBM Watsonx - Coming Soon!")
def show_tasks(): 
    st.info("Enhanced Task Management - Coming Soon!")

# Run the application
if __name__ == "__main__":
    main()
