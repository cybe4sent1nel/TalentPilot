import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time
import random
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="TalentPilot - AI HR Orchestration",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
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
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
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
        background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        box-shadow: 0 10px 30px rgba(249, 115, 22, 0.3);
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
        background: #f97316;
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
        border: 1px solid #e2e8f0;
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
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.15);
    }
    
    .auth-container {
        max-width: 500px;
        margin: 4rem auto;
        background: white;
        border-radius: 30px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid #e2e8f0;
    }
    
    .auth-title {
        font-size: 36px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #1e3a8a 0%, #f97316 100%);
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
        background: linear-gradient(135deg, #1e3a8a 0%, #f97316 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.4);
    }
    
    .response-container {
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 100%);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid #bfdbfe;
        margin-top: 2rem;
    }
    
    .response-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        color: #1e3a8a;
        font-weight: 700;
        font-size: 18px;
    }
    
    .response-content {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        color: #1e293b;
        line-height: 1.7;
        white-space: pre-wrap;
    }
    
    .demo-badge {
        display: inline-block;
        background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin-left: 0.5rem;
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(249, 115, 22, 0.5); }
        50% { box-shadow: 0 0 20px rgba(249, 115, 22, 0.8); }
    }
    
    .activity-item {
        padding: 1rem;
        border-left: 3px solid #e2e8f0;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .activity-item:hover {
        border-left-color: #3b82f6;
        background: #f8fafc;
        border-radius: 0 10px 10px 0;
    }
    
    .module-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px dashed #cbd5e1;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    
    .module-card:hover {
        border-color: #3b82f6;
        background: #f0f9ff;
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
        background: linear-gradient(135deg, #1e3a8a 0%, #f97316 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .chat-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(30, 58, 138, 0.6);
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
        background: #f8fafc;
        border-radius: 12px;
        padding: 1rem;
        min-height: 400px;
    }
    
    .kanban-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #3b82f6;
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
        border-left: 2px solid #e2e8f0;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 0;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #3b82f6;
        border: 2px solid white;
    }
    
    .calendar-day {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.5rem;
        min-height: 80px;
        background: white;
        transition: all 0.3s ease;
    }
    
    .calendar-day:hover {
        background: #f0f9ff;
        border-color: #3b82f6;
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
        'show_onboarding_tour': True
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
        },
        {
            'id': 'EMP003',
            'name': 'Emily Davis',
            'role': 'Sales Director',
            'department': 'Sales',
            'email': 'emily.d@company.com',
            'phone': '+1 (555) 345-6789',
            'hire_date': '2019-01-10',
            'salary': 135000,
            'status': 'Active',
            'manager': 'Robert Brown',
            'location': 'Chicago, IL',
            'skills': ['Sales Strategy', 'CRM', 'Negotiation', 'Team Leadership'],
            'performance_score': 4.8,
            'pto_balance': 8
        },
        {
            'id': 'EMP004',
            'name': 'James Wilson',
            'role': 'HR Specialist',
            'department': 'HR',
            'email': 'james.w@company.com',
            'phone': '+1 (555) 456-7890',
            'hire_date': '2022-05-01',
            'salary': 75000,
            'status': 'On Leave',
            'manager': 'Patricia Lee',
            'location': 'Austin, TX',
            'skills': ['Recruitment', 'Employee Relations', 'HRIS', 'Compliance'],
            'performance_score': 4.0,
            'pto_balance': 3
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
        },
        {
            'id': 'JOB002',
            'title': 'Product Manager',
            'department': 'Product',
            'location': 'San Francisco, CA',
            'type': 'Full-time',
            'salary_range': '$130k - $170k',
            'posted_date': '2024-01-20',
            'applications': 32,
            'status': 'Open',
            'description': 'Seeking a strategic product manager...'
        },
        {
            'id': 'JOB003',
            'title': 'DevOps Engineer',
            'department': 'Engineering',
            'location': 'Hybrid - NYC',
            'type': 'Full-time',
            'salary_range': '$110k - $150k',
            'posted_date': '2024-01-25',
            'applications': 28,
            'status': 'Interviewing',
            'description': 'We need a skilled DevOps engineer...'
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
        },
        {
            'id': 'CAN002',
            'name': 'Jordan Lee',
            'email': 'jordan.l@email.com',
            'phone': '+1 (555) 222-3333',
            'position_applied': 'Product Manager',
            'status': 'Technical Interview',
            'score': 92,
            'experience': '5 years',
            'education': 'MBA + BS Engineering',
            'skills': ['Product Strategy', 'Agile', 'Data Analysis', 'User Research'],
            'resume_url': 'resumes/jordan_lee.pdf',
            'applied_date': '2024-01-21',
            'interview_date': '2024-02-08'
        }
    ]

def generate_notifications():
    return [
        {'id': 1, 'type': 'urgent', 'message': '3 interviews scheduled for today', 'time': '2 hours ago', 'read': False},
        {'id': 2, 'type': 'info', 'message': 'New performance review templates available', 'time': '5 hours ago', 'read': False},
        {'id': 3, 'type': 'success', 'message': '5 new job applications received', 'time': '1 day ago', 'read': True},
        {'id': 4, 'type': 'warning', 'message': '2 employees on leave expiring soon', 'time': '2 days ago', 'read': True}
    ]

def generate_tasks():
    return [
        {'id': 1, 'title': 'Review Sarah Johnson\'s performance', 'priority': 'High', 'due': '2024-02-10', 'status': 'In Progress'},
        {'id': 2, 'title': 'Schedule interviews for PM role', 'priority': 'High', 'due': '2024-02-08', 'status': 'To Do'},
        {'id': 3, 'title': 'Update employee handbook', 'priority': 'Medium', 'due': '2024-02-15', 'status': 'To Do'},
        {'id': 4, 'title': 'Process Q1 bonuses', 'priority': 'High', 'due': '2024-02-20', 'status': 'To Do'},
        {'id': 5, 'title': 'Organize team building event', 'priority': 'Low', 'due': '2024-03-01', 'status': 'Planning'}
    ]

# AI API Call Function with streaming
def call_openrouter_api(prompt, system_message="You are TalentPilot, an expert HR AI assistant. Provide professional, detailed, and actionable HR advice and content."):
    """Call OpenRouter API with error handling"""
    if st.session_state.demo_mode:
        # Demo mode responses with typing effect
        time.sleep(1.5)
        
        if 'job description' in prompt.lower():
            return """**Senior Software Engineer**

**Job Summary:**
We are seeking an experienced Senior Software Engineer to join our dynamic technology team. This role requires a passionate developer with strong technical skills and leadership abilities to drive innovation and mentor junior team members.

**Key Responsibilities:**
• Design and develop scalable web applications using modern frameworks (React, Node.js, Python)
• Lead technical discussions and architectural decisions for complex projects
• Collaborate with cross-functional teams including product, design, and QA
• Mentor junior developers through code reviews and pair programming sessions
• Write clean, maintainable, and well-documented code following best practices
• Participate in sprint planning, daily standups, and retrospectives
• Troubleshoot production issues and optimize application performance

**Required Qualifications:**
• 5+ years of professional software development experience
• Strong proficiency in JavaScript/TypeScript, React, and Node.js
• Experience with RESTful APIs, GraphQL, and microservices architecture
• Solid understanding of database design (SQL and NoSQL)
• Experience with cloud platforms (AWS, Azure, or GCP)
• Excellent problem-solving and communication skills
• Bachelor's degree in Computer Science or equivalent experience

**Preferred Qualifications:**
• Experience with containerization (Docker, Kubernetes)
• Knowledge of DevOps practices and CI/CD pipelines
• Contributions to open-source projects
• Experience with Agile/Scrum methodology
• Leadership or mentorship experience

**What We Offer:**
• Competitive salary range: $120,000 - $160,000
• Equity compensation package
• Comprehensive health, dental, and vision insurance
• 401(k) matching up to 6%
• Flexible work arrangements (hybrid/remote options)
• Professional development budget ($2,000/year)
• Unlimited PTO policy
• Modern tech stack and equipment
• Collaborative and inclusive company culture

**Location:** San Francisco, CA (Hybrid) or Remote

**To Apply:**
Please submit your resume, cover letter, and links to your portfolio or GitHub profile."""
        
        elif 'resume' in prompt.lower() or 'analyze' in prompt.lower():
            return """**📊 COMPREHENSIVE RESUME ANALYSIS REPORT**

**Overall Score: 87/100** ⭐⭐⭐⭐⭐

---

**✅ KEY STRENGTHS:**

1. **Technical Expertise** (9/10)
   - Strong proficiency in modern tech stack (React, Node.js, Python)
   - Demonstrated experience with cloud platforms (AWS, Azure)
   - Solid understanding of both frontend and backend development
   
2. **Leadership & Impact** (8.5/10)
   - Clear evidence of leading technical projects from conception to deployment
   - Mentored 5+ junior developers with measurable performance improvements
   - Drove 40% reduction in page load times through performance optimization
   
3. **Career Progression** (9/10)
   - Steady advancement from Junior to Senior Engineer over 7 years
   - Increasing responsibility and project complexity
   - Consistent track record of delivering high-impact features
   
4. **Quantifiable Achievements** (8/10)
   - "Reduced API response time by 60% through database optimization"
   - "Led migration to microservices, improving system reliability by 45%"
   - "Built CI/CD pipeline that reduced deployment time from 2 hours to 15 minutes"

---

**📈 AREAS FOR IMPROVEMENT:**

1. **Resume Structure** (7/10)
   - Consider adding a professional summary at the top (2-3 sentences)
   - Work experience dates could be more prominent
   - Skills section could be better organized by category

2. **Keyword Optimization** (7.5/10)
   - Missing some key industry terms: "Agile," "Scrum," "DevOps"
   - Could emphasize cloud certifications if available
   - Add more specific framework versions (React 18, Node.js 16, etc.)

3. **Education & Certifications** (6/10)
   - No professional certifications mentioned (AWS Certified, etc.)
   - Consider adding relevant coursework or continuing education
   - GPA could be mentioned if above 3.5

4. **Soft Skills** (7/10)
   - Limited demonstration of communication and collaboration skills
   - Could add more context about cross-functional teamwork
   - Leadership examples could be more detailed

---

**🎯 SKILL MATCH ANALYSIS:**

**For Senior Software Engineer Role:**

| Skill Category | Match Rate | Notes |
|---------------|------------|-------|
| Programming Languages | 95% | Excellent match for required tech stack |
| Cloud & Infrastructure | 90% | Strong AWS/Azure experience |
| Architecture & Design | 85% | Solid microservices background |
| Leadership | 80% | Good mentorship experience |
| DevOps | 75% | Could be stronger in CI/CD |

**Overall Role Fit: 88%** - Excellent Match

---

**💡 RECOMMENDATIONS:**

**Immediate Actions:**
1. Add a compelling professional summary highlighting 7 years of full-stack experience
2. Include 2-3 relevant certifications or list as "In Progress"
3. Reorganize skills section: Frontend | Backend | Cloud | Tools
4. Add links to GitHub profile and portfolio projects

**Interview Focus Areas:**
1. System design and architectural decision-making
2. Leadership scenarios and team mentorship examples
3. Problem-solving approach for complex technical challenges
4. Cultural fit and communication style

**Suggested Questions:**
- "Walk me through your most complex technical project and the architectural decisions you made"
- "How do you approach mentoring junior developers?"
- "Describe a time when you had to make a trade-off between technical excellence and shipping quickly"

---

**🚀 NEXT STEPS:**

**RECOMMENDATION: STRONG HIRE - PROCEED TO INTERVIEW**

This candidate demonstrates excellent technical capabilities, strong career progression, and leadership potential. The combination of hands-on development experience and mentorship makes them an ideal fit for a senior role.

**Action Items:**
1. ✅ Schedule technical phone screen (30 min)
2. ⏭️ System design interview (60 min)
3. ⏭️ Behavioral & cultural fit interview (45 min)
4. ⏭️ Final round with engineering director (30 min)
5. ⏭️ Reference checks (3 references)

**Salary Expectation:** $125K - $145K (based on experience level and location)

**Timeline:** Aim to complete interview process within 2 weeks to avoid losing to competing offers.

---

*This analysis was generated by TalentPilot AI - Your intelligent HR assistant*"""
        
        elif 'interview' in prompt.lower():
            return """**🎤 INTERVIEW QUESTIONS - SENIOR SOFTWARE ENGINEER**

---

**TECHNICAL ASSESSMENT (45 minutes)**

**1. System Design & Architecture**
   
   **Question:** "Design a scalable URL shortening service like bit.ly. Walk me through your architecture, database design, and how you'd handle 10M+ requests per day."
   
   **What to Look For:**
   - Understanding of distributed systems
   - Database sharding strategies
   - Caching mechanisms (Redis, CDN)
   - Load balancing concepts
   - API design principles

---

**2. Coding & Problem Solving**
   
   **Question:** "Implement a rate limiter that allows a maximum of N requests per user per minute. What data structures would you use?"
   
   **What to Look For:**
   - Choice of data structure (sliding window, token bucket)
   - Time complexity analysis
   - Memory efficiency considerations
   - Edge case handling

---

**3. Performance Optimization**
   
   **Question:** "You notice your React application has a slow initial page load. What steps would you take to diagnose and fix the issue?"
   
   **What to Look For:**
   - Knowledge of profiling tools (Lighthouse, Chrome DevTools)
   - Code splitting strategies
   - Lazy loading implementation
   - Bundle size optimization
   - Caching strategies

---

**BEHAVIORAL & LEADERSHIP (30 minutes)**

**4. Team Leadership**
   
   **Question:** "Tell me about a time when you had to convince your team to adopt a new technology or approach that they were initially resistant to."
   
   **What to Look For:**
   - Communication and persuasion skills
   - Data-driven decision making
   - Empathy and understanding of team concerns
   - Change management abilities

---

**5. Conflict Resolution**
   
   **Question:** "Describe a situation where you disagreed with a technical decision made by senior leadership. How did you handle it?"
   
   **What to Look For:**
   - Professional disagreement handling
   - Constructive feedback approach
   - Willingness to escalate appropriately
   - Ability to align with final decisions

---

**6. Mentorship & Growth**
   
   **Question:** "How do you approach code reviews? Give an example of how you helped a junior developer improve their skills."
   
   **What to Look For:**
   - Teaching methodology
   - Patience and empathy
   - Constructive feedback style
   - Investment in team growth

---

**CULTURAL FIT & MOTIVATION (15 minutes)**

**7. Career Goals**
   
   **Question:** "Where do you see yourself in 3-5 years? What skills or experiences are you looking to develop?"
   
   **What to Look For:**
   - Alignment with company growth
   - Continued learning mindset
   - Leadership aspirations
   - Long-term commitment potential

---

**8. Problem-Solving Under Pressure**
   
   **Question:** "Tell me about a time when you had a critical production bug that needed immediate fixing. How did you handle the pressure?"
   
   **What to Look For:**
   - Calm under pressure
   - Systematic debugging approach
   - Communication with stakeholders
   - Post-mortem learning

---

**9. Company Research**
   
   **Question:** "What interests you about our company, and what concerns do you have about joining us?"
   
   **What to Look For:**
   - Research and preparation
   - Genuine interest in mission
   - Honest about concerns
   - Cultural values alignment

---

**10. Technical Curiosity**
   
   **Question:** "What's a technology or framework you've recently learned about or experimented with? What motivated you to explore it?"
   
   **What to Look For:**
   - Continuous learning mindset
   - Self-motivated exploration
   - Practical application thinking
   - Industry awareness

---

**CLOSING QUESTIONS FROM CANDIDATE**

Always allocate time for candidate questions. Quality of questions indicates:
- Interest level and research depth
- Understanding of role complexity
- Career planning maturity
- Cultural priorities

---

**SCORING RUBRIC:**

**Technical Skills (40 points)**
- System Design: ___ /10
- Coding: ___ /10
- Architecture: ___ /10
- Best Practices: ___ /10

**Leadership & Soft Skills (35 points)**
- Communication: ___ /10
- Team Leadership: ___ /10
- Problem Solving: ___ /7
- Mentorship: ___ /8

**Cultural Fit (25 points)**
- Values Alignment: ___ /10
- Growth Mindset: ___ /8
- Team Collaboration: ___ /7

**Total Score: ___ /100**

**Recommendation:**
- 85-100: Strong Hire
- 70-84: Hire
- 60-69: Maybe (discuss with team)
- Below 60: No Hire

---

*Generated by TalentPilot AI - Interview Intelligence System*"""
        
        elif 'onboarding' in prompt.lower():
            return """**🚀 30-DAY ONBOARDING PLAN**

**Employee:** New Marketing Manager
**Department:** Marketing
**Start Date:** [Date]
**Manager:** Head of Marketing
**Buddy:** Senior Marketing Specialist

---

**WEEK 1: ORIENTATION & FOUNDATION** ✨

**Day 1 - Welcome & Setup**
• 9:00 AM - Welcome meeting with HR
• 10:00 AM - IT setup (laptop, email, tools access)
• 11:00 AM - Office tour and introductions
• 12:00 PM - Team lunch
• 2:00 PM - Company overview presentation
• 3:30 PM - Meet with direct manager
• 4:00 PM - Review role expectations and OKRs

**Day 2-3 - Systems & Tools**
• Complete all HR paperwork and benefits enrollment
• Training on key tools: Slack, Asana, Google Workspace, HubSpot
• Access to shared drives and documentation
• Security and compliance training
• Set up 1-on-1s with team members

**Day 4-5 - Deep Dive**
• Review current marketing campaigns
• Analyze past quarter's performance data
• Study competitor analysis reports
• Meet with cross-functional partners (Sales, Product)
• Shadow team members in daily activities

**Week 1 Goals:**
✅ Complete all administrative onboarding
✅ Understand company culture and values
✅ Meet all team members
✅ Set up all necessary tools and access

---

**WEEK 2: LEARNING & INTEGRATION** 📚

**Focus Areas:**
• Deep dive into marketing strategy and positioning
• Understand customer personas and journey mapping
• Review content calendar and campaign pipeline
• Learn budget allocation and ROI tracking

**Key Activities:**
• Attend all team meetings and observe workflows
• Review historical campaign performance
• Meet with key stakeholders (Sales Director, Product Managers)
• Complete industry and market research
• Begin contributing ideas in brainstorming sessions

**Deliverable:** 
📄 "First Impressions" document with observations and initial ideas

**Week 2 Goals:**
✅ Understand current marketing initiatives
✅ Identify quick wins and opportunities
✅ Build relationships with stakeholders
✅ Complete product/service training

---

**WEEK 3: CONTRIBUTING & COLLABORATING** 🎯

**Focus Areas:**
• Start taking ownership of specific projects
• Lead first team meeting or standup
• Begin executing on assigned campaigns
• Contribute to strategy discussions

**Key Activities:**
• Take lead on one small marketing campaign
• Collaborate on content creation
• Attend customer calls or focus groups
• Present findings from market research
• Start managing vendor relationships

**Deliverable:**
📊 30-60-90 Day Plan presentation

**Week 3 Goals:**
✅ Lead first project end-to-end
✅ Demonstrate strategic thinking
✅ Show measurable progress on initiatives
✅ Establish working rhythm with team

---

**WEEK 4: OWNERSHIP & IMPACT** 💪

**Focus Areas:**
• Full ownership of key marketing initiatives
• Drive strategy for upcoming quarter
• Optimize existing campaigns
• Begin measuring and reporting on KPIs

**Key Activities:**
• Present strategy recommendations to leadership
• Launch first major campaign
• Conduct team workshop or training
• Set OKRs for next quarter
• Complete 30-day feedback session with manager

**Deliverable:**
📈 First campaign results and learnings presentation

**Week 4 Goals:**
✅ Deliver measurable business impact
✅ Demonstrate leadership capabilities
✅ Complete 30-day performance review
✅ Finalize 60-90 day objectives

---

**ONGOING THROUGHOUT 30 DAYS**

**Weekly Check-ins:**
• Monday: Week planning with manager (30 min)
• Wednesday: Buddy coffee chat (informal)
• Friday: Week review and feedback (15 min)

**Training & Development:**
• Complete 5 LinkedIn Learning courses on marketing trends
• Read company's recommended books/resources
• Attend 2 industry webinars or events
• Shadow different departments (1 day each: Sales, Product, CS)

**Networking:**
• Schedule 1-on-1s with 15+ team members across departments
• Attend all company all-hands and team socials
• Join relevant Slack channels and engage actively

---

**SUCCESS METRICS (30-DAY CHECKPOINT)**

**Performance Indicators:**
✅ Completed all onboarding tasks (100%)
✅ Launched at least 1 campaign
✅ Positive feedback from team and stakeholders
✅ Demonstrated understanding of business goals
✅ Shown initiative and strategic thinking
✅ Built strong relationships across teams

**Knowledge Assessment:**
□ Can articulate company mission and values
□ Understands target customer deeply
□ Knows all team members and their roles
□ Comfortable with all marketing tools
□ Clear on quarterly and annual goals

---

**SUPPORT RESOURCES**

**Your Onboarding Team:**
• Manager: Weekly 1-on-1s and guidance
• Buddy: Daily questions and peer support
• HR Partner: Benefits, policies, and culture
• IT Support: Technical issues

**Documentation:**
• Employee Handbook (Intranet)
• Marketing Playbook (Google Drive)
• Brand Guidelines (Figma)
• Product Documentation (Confluence)

**Feedback Checkpoints:**
• Day 7: First week reflection
• Day 14: Two-week check-in
• Day 30: Comprehensive review
• Day 60: Performance milestone
• Day 90: Full integration assessment

---

**MANAGER RESPONSIBILITIES**

**Before Day 1:**
✅ Prepare welcome email and schedule
✅ Set up workspace and equipment
✅ Assign buddy and notify team
✅ Prepare onboarding materials

**First Week:**
✅ Daily check-ins
✅ Clear goal setting
✅ Team introductions facilitation
✅ Answer questions and provide context

**Ongoing:**
✅ Weekly 1-on-1 meetings
✅ Regular feedback and coaching
✅ Remove blockers and provide support
✅ Celebrate early wins

---

**🎉 WELCOME TO THE TEAM!**

*This onboarding plan is designed to set you up for success. Remember: asking questions is encouraged, making mistakes is part of learning, and we're all here to support you!*

---

*Generated by TalentPilot AI - Onboarding Excellence Platform*"""
        
        else:
            return """**🤖 TalentPilot AI Assistant**

Hello! I'm your AI-powered HR co-pilot. I can help you with:

**📝 Recruitment & Hiring**
• Generate professional job descriptions
• Analyze and score candidate resumes
• Create interview questions and assessment rubrics
• Design candidate evaluation frameworks
• Provide salary benchmarking insights

**👥 Employee Management**
• Create onboarding plans and checklists
• Generate performance review templates
• Design 360-degree feedback surveys
• Build career development pathways
• Create recognition and reward programs

**📊 HR Operations**
• Draft HR policies and procedures
• Design compensation and benefits packages
• Create leave management policies
• Generate compliance documentation
• Build employee engagement surveys

**🎓 Learning & Development**
• Create training programs and curriculums
• Design skills gap analysis frameworks
• Build learning paths for career progression
• Generate workshop content and materials
• Create mentorship program structures

**💡 Strategic HR**
• Workforce planning and forecasting
• Organizational design recommendations
• Culture and engagement strategies
• Diversity and inclusion initiatives
• Change management frameworks

**How can I assist you today?**

Simply describe what you need, and I'll provide detailed, actionable guidance. I can generate documents, analyze data, provide strategic recommendations, and help you make better HR decisions.

Try asking me to:
- "Generate a job description for [role]"
- "Analyze this resume for [position]"
- "Create interview questions for [role]"
- "Design an onboarding plan for [position]"
- "Help me with [specific HR challenge]"

*I'm here to make your HR processes more efficient and effective!*"""
    
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
                        👥
                        <div class="logo-accent">🎯</div>
                    </div>
                </div>
            </div>
            <h1 class="auth-title">TalentPilot</h1>
            <p class="auth-subtitle">Your AI Co-Pilot for Modern HR Management</p>
        </div>
        """, unsafe_allow_html=True)
        
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
            <h3 style="color: #1e3a8a; margin-bottom: 1rem;">✨ Key Features</h3>
        </div>
        """, unsafe_allow_html=True)
        
        features = [
            {"icon": "🤖", "title": "AI-Powered", "desc": "Advanced AI for all HR tasks"},
            {"icon": "⚡", "title": "Fast & Efficient", "desc": "Automate repetitive work"},
            {"icon": "📊", "title": "Data-Driven", "desc": "Analytics and insights"},
            {"icon": "🔒", "title": "Secure", "desc": "Enterprise-grade security"}
        ]
        
        col1, col2, col3, col4 = st.columns(4)
        for col, feat in zip([col1, col2, col3, col4], features):
            with col:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 32px;">{feat['icon']}</div>
                    <div style="font-weight: 600; color: #1e293b; margin-top: 0.5rem;">{feat['title']}</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 0.25rem;">{feat['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 13px;">
            <p><strong>Secure • AI-Powered • Enterprise-Ready</strong></p>
            <p style="margin-top: 0.5rem;">Demo mode lets you explore all features with sample data</p>
        </div>
        """, unsafe_allow_html=True)

# Sidebar with notifications
def show_sidebar():
    """Display enhanced sidebar with navigation"""
    with st.sidebar:
        # Logo Section
        st.markdown("""
        <div class="logo-container">
            <div class="logo-box">
                👥
                <div class="logo-accent">🎯</div>
            </div>
            <div class="logo-text">TalentPilot</div>
        </div>
        """, unsafe_allow_html=True)
        
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
            <div style="background: rgba(249, 115, 22, 0.2); border: 2px solid #fb923c; 
                        border-radius: 10px; padding: 0.75rem; text-align: center; margin-bottom: 1rem;">
                <span style="color: white; font-weight: 700;">🎮 DEMO MODE</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Notifications
        unread_count = sum(1 for n in st.session_state.notifications if not n['read'])
        if unread_count > 0:
            with st.expander(f"🔔 Notifications ({unread_count})", expanded=False):
                for notif in st.session_state.notifications[:3]:
                    if not notif['read']:
                        st.markdown(f"**{notif['message']}**")
                        st.caption(notif['time'])
                        st.markdown("---")
        
        # Navigation Menu
        st.markdown("### 📋 Modules")
        
        pages = {
            "🏠 Dashboard": "Dashboard",
            "👥 Recruitment": "Recruitment",
            "📋 Onboarding": "Onboarding",
            "💼 Employee Directory": "Employee Directory",
            "🎯 Performance": "Performance Reviews",
            "🎓 Training": "Training & Development",
            "💰 Compensation": "Compensation",
            "📅 Leave": "Leave Management",
            "🚪 Offboarding": "Offboarding",
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
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        st.metric("Employees", st.session_state.employee_count)
        st.metric("Open Positions", len(st.session_state.job_postings))
        st.metric("Pending Tasks", len([t for t in st.session_state.tasks if t['status'] != 'Done']))
        
        st.markdown("---")
        
        # Settings and Logout
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚙️", use_container_width=True, help="Settings"):
                st.info("Settings panel coming soon!")
        
        with col2:
            if st.button("🚪", use_container_width=True, help="Logout"):
                st.session_state.authenticated = False
                st.session_state.api_key = ''
                st.session_state.demo_mode = False
                st.rerun()

# Enhanced Dashboard
def show_dashboard():
    """Display enhanced dashboard with more insights"""
    # Header with greeting
    current_hour = datetime.now().hour
    greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"
    
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #1e293b; margin-bottom: 0.5rem;">
            {greeting}, {st.session_state.user_name}! 👋
            {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}
        </h1>
        <p style="color: #64748b; font-size: 16px;">Here's what's happening with your team today</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        {"icon": "👥", "value": "1,234", "label": "Total Employees", "change": "+12% from last month", "color": "#3b82f6"},
        {"icon": "💼", "value": "23", "label": "Open Positions", "change": "+5 new this week", "color": "#f97316"},
        {"icon": "🎯", "value": "45", "label": "Pending Reviews", "change": "15 due this week", "color": "#10b981"},
        {"icon": "🎓", "value": "78%", "label": "Training Progress", "change": "+8% completion", "color": "#8b5cf6"},
        {"icon": "😊", "value": "8.4", "label": "Satisfaction Score", "change": "+0.3 points", "color": "#ec4899"}
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
                <div style="color: #10b981; font-size: 11px; font-weight: 600; text-align: center;">
                    ↗ {stat['change']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content area
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Recent Activity
        st.markdown("### 📊 Recent Activity")
        
        activities = [
            {"title": "New hire onboarded", "name": "Sarah Johnson - Software Engineer", "time": "2 hours ago", "color": "#10b981", "icon": "✅"},
            {"title": "Interview scheduled", "name": "Michael Chen - Product Manager", "time": "5 hours ago", "color": "#3b82f6", "icon": "📅"},
            {"title": "Performance review completed", "name": "Emily Davis - Sales Director", "time": "1 day ago", "color": "#10b981", "icon": "⭐"},
            {"title": "Leave request pending", "name": "James Wilson - 3 days vacation", "time": "2 days ago", "color": "#f59e0b", "icon": "⏳"},
            {"title": "Training completed", "name": "5 employees finished Leadership Training", "time": "3 days ago", "color": "#8b5cf6", "icon": "🎓"}
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div class="activity-item">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 24px;">{activity['icon']}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.25rem;">{activity['title']}</div>
                        <div style="color: #64748b; font-size: 14px;">{activity['name']}</div>
                    </div>
                    <div style="color: #94a3b8; font-size: 12px; white-space: nowrap;">{activity['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Upcoming Events
        st.markdown("### 📅 Upcoming This Week")
        
        events = [
            {"date": "Today, 2:00 PM", "title": "Interview: Senior Developer", "type": "Meeting"},
            {"date": "Tomorrow, 10:00 AM", "title": "Performance Reviews Due", "type": "Deadline"},
            {"date": "Thu, 3:00 PM", "title": "Team All-Hands Meeting", "type": "Meeting"},
            {"date": "Fri, EOD", "title": "Q1 Hiring Report", "type": "Deadline"}
        ]
        
        for event in events:
            col_date, col_event = st.columns([1, 3])
            with col_date:
                st.markdown(f"**{event['date']}**")
            with col_event:
                st.markdown(f"{event['title']} `{event['type']}`")
    
    with col_right:
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📝 Post New Job", use_container_width=True):
            st.session_state.current_page = "Recruitment"
            st.rerun()
        
        if st.button("👤 Add Employee", use_container_width=True):
            st.session_state.current_page = "Employee Directory"
            st.rerun()
        
        if st.button("📋 Create Review", use_container_width=True):
            st.session_state.current_page = "Performance Reviews"
            st.rerun()
        
        if st.button("💬 Ask AI Assistant", use_container_width=True):
            st.session_state.current_page = "AI Assistant"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tasks Summary
        st.markdown("### ✅ Your Tasks")
        
        priority_tasks = [t for t in st.session_state.tasks if t['priority'] == 'High'][:3]
        
        for task in priority_tasks:
            with st.container():
                col_check, col_task = st.columns([1, 10])
                with col_check:
                    st.checkbox("", key=f"task_{task['id']}", label_visibility="collapsed")
                with col_task:
                    st.markdown(f"**{task['title']}**")
                    st.caption(f"Due: {task['due']} • {task['status']}")
        
        if st.button("View All Tasks →", use_container_width=True):
            st.session_state.current_page = "Tasks"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Team Pulse
        st.markdown("### 💓 Team Pulse")
        
        pulse_data = [
            {"metric": "Engagement", "value": 85, "trend": "up"},
            {"metric": "Satisfaction", "value": 84, "trend": "up"},
            {"metric": "Productivity", "value": 92, "trend": "stable"},
            {"metric": "Well-being", "value": 78, "trend": "up"}
        ]
        
        for item in pulse_data:
            col_metric, col_value = st.columns([2, 1])
            with col_metric:
                st.markdown(f"**{item['metric']}**")
            with col_value:
                trend_icon = "📈" if item['trend'] == "up" else "📊" if item['trend'] == "stable" else "📉"
                st.markdown(f"{item['value']}% {trend_icon}")

# Employee Directory Page
def show_employee_directory():
    """Display comprehensive employee directory"""
    st.markdown(f"## 💼 Employee Directory {'<span class=\"demo-badge\">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Manage and view all employee information")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search employees", placeholder="Name, role, department, skills...")
    
    with col2:
        dept_filter = st.selectbox("Department", ["All"] + list(set([e['department'] for e in st.session_state.employees])))
    
    with col3:
        status_filter = st.selectbox("Status", ["All", "Active", "On Leave", "Remote"])
    
    with col4:
        sort_by = st.selectbox("Sort by", ["Name", "Department", "Hire Date", "Salary"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # View toggle
    col1, col2, col3 = st.columns([1, 1, 8])
    with col1:
        view_mode = st.radio("View", ["Cards", "Table"], horizontal=True, label_visibility="collapsed")
    
    with col3:
        if st.button("➕ Add New Employee", type="primary"):
            st.info("Employee creation form coming in next update!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter employees
    filtered_employees = st.session_state.employees
    
    if search_term:
        filtered_employees = [e for e in filtered_employees if 
                             search_term.lower() in e['name'].lower() or 
                             search_term.lower() in e['role'].lower() or
                             search_term.lower() in e['department'].lower()]
    
    if dept_filter != "All":
        filtered_employees = [e for e in filtered_employees if e['department'] == dept_filter]
    
    if status_filter != "All":
        filtered_employees = [e for e in filtered_employees if e['status'] == status_filter]
    
    # Display employees
    if view_mode == "Cards":
        # Card view
        cols = st.columns(2)
        for idx, emp in enumerate(filtered_employees):
            col = cols[idx % 2]
            with col:
                with st.container():
                    st.markdown(f"""
                    <div class="feature-card">
                        <div style="display: flex; gap: 1.5rem;">
                            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                        font-size: 36px; color: white; flex-shrink: 0;">
                                {emp['name'][0]}
                            </div>
                            <div style="flex: 1;">
                                <div style="font-weight: 700; color: #1e293b; font-size: 20px; margin-bottom: 0.25rem;">
                                    {emp['name']}
                                </div>
                                <div style="color: #3b82f6; font-weight: 600; font-size: 14px; margin-bottom: 0.5rem;">
                                    {emp['role']}
                                </div>
                                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem;">
                                    <span style="padding: 0.25rem 0.75rem; background: #dcfce7; color: #166534; 
                                                border-radius: 12px; font-size: 12px; font-weight: 600;">
                                        {emp['status']}
                                    </span>
                                    <span style="padding: 0.25rem 0.75rem; background: #fef3c7; color: #92400e; 
                                                border-radius: 12px; font-size: 12px; font-weight: 600;">
                                        ⭐ {emp['performance_score']}
                                    </span>
                                </div>
                                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; 
                                            font-size: 13px; color: #64748b; margin-bottom: 1rem;">
                                    <div>📧 {emp['email']}</div>
                                    <div>📞 {emp['phone']}</div>
                                    <div>📅 Joined: {emp['hire_date']}</div>
                                    <div>📍 {emp['location']}</div>
                                </div>
                                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                                    {' '.join([f'<span style="padding: 0.2rem 0.5rem; background: #f1f5f9; color: #475569; border-radius: 6px; font-size: 11px;">{skill}</span>' for skill in emp['skills'][:4]])}
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("View Profile", key=f"view_{emp['id']}", use_container_width=True):
                            show_employee_profile(emp)
                    with col2:
                        if st.button("Edit", key=f"edit_{emp['id']}", use_container_width=True):
                            st.info("Edit functionality coming soon!")
                    with col3:
                        if st.button("Contact", key=f"contact_{emp['id']}", use_container_width=True):
                            st.info(f"Email: {emp['email']}\nPhone: {emp['phone']}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
    else:
        # Table view
        import pandas as pd
        df = pd.DataFrame(filtered_employees)
        display_df = df[['name', 'role', 'department', 'status', 'email', 'hire_date', 'performance_score']]
        display_df.columns = ['Name', 'Role', 'Department', 'Status', 'Email', 'Hire Date', 'Performance']
        st.dataframe(display_df, use_container_width=True, height=400)

def show_employee_profile(employee):
    """Show detailed employee profile in a modal-style view"""
    with st.expander("📋 Full Employee Profile", expanded=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="width: 150px; height: 150px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                            border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                            font-size: 72px; color: white; margin: 0 auto 1rem;">
                    {employee['name'][0]}
                </div>
                <h3 style="color: #1e293b; margin-bottom: 0.5rem;">{employee['name']}</h3>
                <p style="color: #3b82f6; font-weight: 600;">{employee['role']}</p>
                <p style="color: #64748b;">ID: {employee['id']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📊 Overview")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Department", employee['department'])
                st.metric("Manager", employee['manager'])
                st.metric("Performance", f"{employee['performance_score']}/5.0")
            
            with col_b:
                st.metric("Status", employee['status'])
                st.metric("Location", employee['location'])
                st.metric("PTO Balance", f"{employee['pto_balance']} days")
            
            st.markdown("### 💼 Details")
            st.write(f"**Email:** {employee['email']}")
            st.write(f"**Phone:** {employee['phone']}")
            st.write(f"**Hire Date:** {employee['hire_date']}")
            st.write(f"**Salary:** ${employee['salary']:,}/year")
            
            st.markdown("### 🎯 Skills")
            st.write(" • ".join(employee['skills']))

# Recruitment Page (Enhanced)
def show_recruitment():
    """Enhanced recruitment module with applicant tracking"""
    st.markdown(f"## 👥 Recruitment Hub {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("AI-powered hiring and candidate management")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recruitment metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Open Positions", len(st.session_state.job_postings), "+3")
    with col2:
        st.metric("Total Applications", sum(j['applications'] for j in st.session_state.job_postings), "+15")
    with col3:
        st.metric("In Interview", len([c for c in st.session_state.candidates if 'Interview' in c['status']]), "+2")
    with col4:
        st.metric("Avg. Time to Hire", "28 days", "-4")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Job Postings", 
        "🎯 Candidates", 
        "✨ AI Tools",
        "📊 Pipeline",
        "📈 Analytics"
    ])
    
    with tab1:
        st.markdown("### Active Job Postings")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("➕ Post New Job", type="primary", use_container_width=True):
                st.session_state.show_job_form = True
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for job in st.session_state.job_postings:
            with st.container():
                st.markdown(f"""
                <div class="feature-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h3 style="color: #1e3a8a; margin-bottom: 0.5rem;">{job['title']}</h3>
                            <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;">
                                <span style="color: #64748b;">📍 {job['location']}</span>
                                <span style="color: #64748b;">💼 {job['type']}</span>
                                <span style="color: #64748b;">💰 {job['salary_range']}</span>
                                <span style="color: #64748b;">📅 Posted: {job['posted_date']}</span>
                            </div>
                            <div style="display: flex; gap: 0.5rem; align-items: center;">
                                <span style="padding: 0.25rem 0.75rem; background: #dcfce7; color: #166534; 
                                            border-radius: 12px; font-size: 12px; font-weight: 600;">
                                    {job['status']}
                                </span>
                                <span style="padding: 0.25rem 0.75rem; background: #dbeafe; color: #1e40af; 
                                            border-radius: 12px; font-size: 12px; font-weight: 600;">
                                    {job['applications']} Applications
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("View Details", key=f"view_{job['id']}", use_container_width=True):
                        st.info(job['description'])
                with col2:
                    if st.button("View Applicants", key=f"applicants_{job['id']}", use_container_width=True):
                        st.info(f"{job['applications']} applicants for this position")
                with col3:
                    if st.button("Edit", key=f"edit_{job['id']}", use_container_width=True):
                        st.info("Edit functionality coming soon!")
                with col4:
                    if st.button("Close Position", key=f"close_{job['id']}", use_container_width=True):
                        st.warning("Are you sure you want to close this position?")
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Candidate Pipeline")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            position_filter = st.selectbox("Position", ["All"] + list(set([c['position_applied'] for c in st.session_state.candidates])))
        with col2:
            status_filter = st.selectbox("Stage", ["All", "Phone Screen", "Technical Interview", "Final Round", "Offer"])
        with col3:
            score_filter = st.slider("Min Score", 0, 100, 0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display candidates
        for candidate in st.session_state.candidates:
            with st.container():
                st.markdown(f"""
                <div class="feature-card">
                    <div style="display: flex; gap: 1.5rem; align-items: start;">
                        <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #f97316, #fb923c); 
                                    border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                    font-size: 28px; color: white;">
                            {candidate['name'][0]}
                        </div>
                        <div style="flex: 1;">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div>
                                    <h4 style="color: #1e293b; margin-bottom: 0.25rem;">{candidate['name']}</h4>
                                    <p style="color: #3b82f6; font-weight: 600; margin-bottom: 0.5rem;">
                                        {candidate['position_applied']}
                                    </p>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-size: 24px; font-weight: 800; color: #10b981;">
                                        {candidate['score']}
                                    </div>
                                    <div style="font-size: 12px; color: #64748b;">AI Score</div>
                                </div>
                            </div>
                            <div style="display: flex; gap: 1rem; margin-bottom: 0.75rem; font-size: 13px; color: #64748b;">
                                <span>📧 {candidate['email']}</span>
                                <span>📞 {candidate['phone']}</span>
                                <span>🎓 {candidate['education']}</span>
                                <span>💼 {candidate['experience']}</span>
                            </div>
                            <div style="display: flex; gap: 0.5rem; margin-bottom: 0.75rem;">
                                <span style="padding: 0.25rem 0.75rem; background: #fef3c7; color: #92400e; 
                                            border-radius: 12px; font-size: 12px; font-weight: 600;">
                                    {candidate['status']}
                                </span>
                                <span style="padding: 0.25rem 0.75rem; background: #f3f4f6; color: #4b5563; 
                                            border-radius: 12px; font-size: 12px;">
                                    Applied: {candidate['applied_date']}
                                </span>
                            </div>
                            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                                {' '.join([f'<span style="padding: 0.2rem 0.5rem; background: #f1f5f9; color: #475569; border-radius: 6px; font-size: 11px;">{skill}</span>' for skill in candidate['skills']])}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("View Resume", key=f"resume_{candidate['id']}", use_container_width=True):
                        st.info("Resume viewer coming soon!")
                with col2:
                    if st.button("Schedule Interview", key=f"schedule_{candidate['id']}", use_container_width=True):
                        st.success(f"Interview scheduled for {candidate['interview_date']}")
                with col3:
                    if st.button("Send Email", key=f"email_{candidate['id']}", use_container_width=True):
                        st.info("Email composer coming soon!")
                with col4:
                    if st.button("Move to Next Stage", key=f"advance_{candidate['id']}", use_container_width=True, type="primary"):
                        st.success("Candidate advanced!")
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🤖 AI-Powered Recruitment Tools")
        
        tool_tabs = st.tabs(["📝 Job Description", "🎯 Resume Analyzer", "💬 Interview Questions"])
        
        with tool_tabs[0]:
            st.markdown("#### Generate Professional Job Descriptions")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                job_input = st.text_area(
                    "Job Details",
                    placeholder="Enter job title and key details (e.g., 'Senior Software Engineer with 5 years experience in React and Node.js')",
                    height=150,
                    help="Provide basic information about the role"
                )
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✨ Generate Job Description", use_container_width=True, type="primary"):
                        if job_input:
                            with st.spinner("🤖 AI is crafting your job description..."):
                                prompt = f"Generate a comprehensive job description for: {job_input}. Include: job title, summary, key responsibilities, required qualifications, preferred qualifications, and benefits."
                                response = call_openrouter_api(prompt)
                                
                                st.markdown(f"""
                                <div class="response-container success-animation">
                                    <div class="response-header">
                                        ✅ Generated Job Description
                                    </div>
                                    <div class="response-content">
                                        {response}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.warning("Please enter job details first")
                
                with col_btn2:
                    if st.button("📋 Save as Draft", use_container_width=True):
                        st.success("Draft saved!")
            
            with col2:
                st.info("""
                **💡 Pro Tips:**
                
                • Include job title
                • Mention experience level
                • List key technologies
                • Specify team size
                • Note location/remote options
                • Add salary range if possible
                
                **Best for:**
                - Tech roles
                - Marketing positions
                - Sales roles
                - Management positions
                """)
        
        with tool_tabs[1]:
            st.markdown("#### AI-Powered Resume Analysis")
            
            resume_text = st.text_area(
                "Resume Content",
                placeholder="Paste resume text here for comprehensive AI analysis...",
                height=200,
                help="Copy and paste the resume content for detailed analysis"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔍 Analyze Resume", use_container_width=True, type="primary"):
                    if resume_text:
                        with st.spinner("🤖 AI is analyzing the resume..."):
                            prompt = f"Analyze this resume and provide: 1) Overall score (0-100), 2) Key strengths, 3) Areas for improvement, 4) Skill match analysis, 5) Recommendation.\n\nResume:\n{resume_text}"
                            response = call_openrouter_api(prompt)
                            
                            st.markdown(f"""
                            <div class="response-container success-animation">
                                <div class="response-header">
                                    ✅ Resume Analysis Complete
                                </div>
                                <div class="response-content">
                                    {response}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("Please paste resume content first")
            
            with col2:
                if st.button("📄 Upload Resume (PDF)", use_container_width=True):
                    st.info("PDF upload feature coming soon!")
            
            with col3:
                if st.button("💾 Save Analysis", use_container_width=True):
                    st.success("Analysis saved to candidate profile!")
        
        with tool_tabs[2]:
            st.markdown("#### Generate Interview Questions")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                role_input = st.text_input(
                    "Role/Position",
                    placeholder="e.g., Senior Product Manager",
                    help="Enter the role you're interviewing for"
                )
                
                interview_type = st.selectbox(
                    "Interview Type",
                    ["Technical Interview", "Behavioral Interview", "Leadership Interview", "Cultural Fit", "General Assessment"]
                )
                
                num_questions = st.slider("Number of Questions", 5, 20, 10)
                
                if st.button("🎤 Generate Questions", use_container_width=True, type="primary"):
                    if role_input:
                        with st.spinner("🤖 Creating interview questions..."):
                            prompt = f"Generate {num_questions} insightful {interview_type} questions for a {role_input} position. Include a mix of difficulty levels and provide brief guidance on what to look for in answers."
                            response = call_openrouter_api(prompt)
                            
                            st.markdown(f"""
                            <div class="response-container success-animation">
                                <div class="response-header">
                                    ✅ Interview Questions Ready
                                </div>
                                <div class="response-content">
                                    {response}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("Please enter the role first")
            
            with col2:
                st.info("""
                **📝 Question Types:**
                
                **Technical**
                - Coding challenges
                - System design
                - Problem-solving
                
                **Behavioral**
                - Past experiences
                - Conflict resolution
                - Team collaboration
                
                **Leadership**
                - Team management
                - Strategic thinking
                - Decision-making
                
                **Cultural Fit**
                - Values alignment
                - Work style
                - Company goals
                """)
    
    with tab4:
        st.markdown("### 📊 Recruitment Pipeline")
        
        # Kanban-style pipeline
        stages = {
            "📨 New Applications": 12,
            "📞 Phone Screen": 8,
            "💻 Technical Interview": 5,
            "👔 Final Round": 3,
            "✅ Offer Stage": 2
        }
        
        cols = st.columns(len(stages))
        
        for col, (stage, count) in zip(cols, stages.items()):
            with col:
                st.markdown(f"""
                <div class="kanban-column">
                    <h4 style="color: #1e293b; margin-bottom: 1rem;">{stage}</h4>
                    <div style="text-align: center; font-size: 32px; font-weight: 800; color: #3b82f6; margin-bottom: 1rem;">
                        {count}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                for i in range(min(count, 3)):
                    st.markdown(f"""
                    <div class="kanban-card">
                        <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.25rem;">
                            Candidate #{i+1}
                        </div>
                        <div style="font-size: 12px; color: #64748b;">
                            Applied 2 days ago
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### 📈 Recruitment Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📊 Sources")
            st.write("• LinkedIn: 45%")
            st.write("• Indeed: 30%")
            st.write("• Referrals: 15%")
            st.write("• Company Site: 10%")
        
        with col2:
            st.markdown("#### ⏱️ Time Metrics")
            st.metric("Avg. Time to Hire", "28 days")
            st.metric("Avg. Time to Screen", "3 days")
            st.metric("Avg. Time to Offer", "21 days")
        
        with col3:
            st.markdown("#### 💰 Cost Metrics")
            st.metric("Cost per Hire", "$4,200")
            st.metric("Total Recruitment Cost", "$84,000")
            st.metric("ROI", "3.2x")

# Tasks Management Page
def show_tasks():
    """Task management and to-do list"""
    st.markdown(f"## 📋 Task Management {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Manage your HR tasks and priorities")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Task stats
    col1, col2, col3, col4 = st.columns(4)
    
    total_tasks = len(st.session_state.tasks)
    completed = len([t for t in st.session_state.tasks if t['status'] == 'Done'])
    in_progress = len([t for t in st.session_state.tasks if t['status'] == 'In Progress'])
    high_priority = len([t for t in st.session_state.tasks if t['priority'] == 'High'])
    
    with col1:
        st.metric("Total Tasks", total_tasks)
    with col2:
        st.metric("Completed", completed, f"{int(completed/total_tasks*100)}%")
    with col3:
        st.metric("In Progress", in_progress)
    with col4:
        st.metric("High Priority", high_priority)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add new task
    with st.expander("➕ Add New Task", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_task_title = st.text_input("Task Title", placeholder="Enter task description...")
            new_task_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        with col2:
            new_task_due = st.date_input("Due Date")
            new_task_status = st.selectbox("Status", ["To Do", "In Progress", "Planning", "Done"])
        
        if st.button("Add Task", type="primary"):
            st.success("✅ Task added successfully!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter and sort
    col1, col2, col3 = st.columns(3)
    with col1:
        priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "To Do", "In Progress", "Planning", "Done"])
    with col3:
        sort_option = st.selectbox("Sort by", ["Due Date", "Priority", "Status"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display tasks in kanban columns
    col1, col2, col3, col4 = st.columns(4)
    
    statuses = ["To Do", "In Progress", "Planning", "Done"]
    columns = [col1, col2, col3, col4]
    
    for col, status in zip(columns, statuses):
        with col:
            st.markdown(f"### {status}")
            tasks_in_status = [t for t in st.session_state.tasks if t['status'] == status]
            
            for task in tasks_in_status:
                priority_color = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#3b82f6"}[task['priority']]
                
                st.markdown(f"""
                <div class="kanban-card" style="border-left-color: {priority_color};">
                    <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.5rem;">
                        {task['title']}
                    </div>
                    <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="padding: 0.15rem 0.5rem; background: {priority_color}20; color: {priority_color}; 
                                    border-radius: 6px; font-size: 11px; font-weight: 600;">
                            {task['priority']}
                        </span>
                    </div>
                    <div style="font-size: 12px; color: #64748b;">
                        📅 Due: {task['due']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("✏️", key=f"edit_task_{task['id']}", help="Edit task"):
                    st.info("Task editor coming soon!")

# AI Assistant Page
def show_ai_assistant():
    """Interactive AI assistant with chat interface"""
    st.markdown(f"## 💬 AI Assistant {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Your intelligent HR co-pilot powered by advanced AI")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Suggested prompts
    st.markdown("### 💡 Try these prompts:")
    
    prompts = [
        "Generate a job description for a Data Scientist",
        "Create an onboarding plan for a new Marketing Manager",
        "What are best practices for conducting performance reviews?",
        "Help me design a compensation package for senior engineers",
        "Create interview questions for a Product Manager role"
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat history display
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation")
        
        for idx, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; 
                                padding: 1rem; border-radius: 15px; max-width: 70%; border-bottom-right-radius: 5px;">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                    <div style="background: #f1f5f9; color: #1e293b; padding: 1rem; 
                                border-radius: 15px; max-width: 80%; border-bottom-left-radius: 5px;">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Ask me anything about HR...",
            placeholder="Type your question here...",
            label_visibility="collapsed",
            key="ai_chat_input"
        )
    with col2:
        send_button = st.button("Send 🚀", type="primary", use_container_width=True)
    
    if send_button and user_input:
        with st.spinner("🤖 Thinking..."):
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            response = call_openrouter_api(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

# Additional placeholder modules for completeness
def show_onboarding():
    """Onboarding module"""
    st.markdown(f"## 📋 Onboarding {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Create seamless onboarding experiences")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Create Plan", "📊 Active Plans"])
    
    with tab1:
        st.markdown("### 🚀 Generate Onboarding Plan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_hire_role = st.text_input("New Hire Role", placeholder="e.g., Marketing Manager")
            department = st.selectbox("Department", ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations", "Product"])
            start_date = st.date_input("Start Date")
            
            if st.button("✨ Generate Onboarding Plan", use_container_width=True, type="primary"):
                if new_hire_role:
                    with st.spinner("🤖 Creating personalized onboarding plan..."):
                        prompt = f"Create a comprehensive 30-day onboarding plan for a new {new_hire_role} in the {department} department. Include: Week 1-4 activities, key meetings, training sessions, goals, and success metrics."
                        response = call_openrouter_api(prompt)
                        
                        st.markdown(f"""
                        <div class="response-container success-animation">
                            <div class="response-header">
                                ✅ Onboarding Plan Ready
                            </div>
                            <div class="response-content">
                                {response}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Please enter the new hire role")
        
        with col2:
            st.info("""
            **📌 Best Practices:**
            
            • Start before day one
            • Clear 30-60-90 day goals
            • Regular check-ins
            • Assign buddy/mentor
            • Gather feedback
            • Celebrate milestones
            """)
    
    with tab2:
        st.markdown("### 📊 Active Onboarding Plans")
        st.info("Track progress of new hires currently in onboarding")

def show_performance():
    """Performance management module"""
    st.markdown(f"## 🎯 Performance Reviews {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("360-degree feedback and goal tracking")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Create Review", "🎯 Goal Setting"])
    
    with tab1:
        st.markdown("### AI-Powered Review Generator")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            employee_name = st.text_input("Employee Name", placeholder="John Doe")
            position = st.text_input("Position", placeholder="Software Engineer")
            review_period = st.selectbox("Review Period", ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Annual 2024"])
            
            strengths = st.text_area(
                "Key Achievements & Strengths",
                placeholder="List major accomplishments...",
                height=100
            )
            
            improvements = st.text_area(
                "Areas for Development",
                placeholder="Skills to develop...",
                height=100
            )
            
            if st.button("✨ Generate Review", use_container_width=True, type="primary"):
                if employee_name and strengths:
                    with st.spinner("🤖 Creating review..."):
                        prompt = f"Create a professional performance review for {employee_name}, {position} for {review_period}.\n\nStrengths:\n{strengths}\n\nDevelopment:\n{improvements}"
                        response = call_openrouter_api(prompt)
                        
                        st.markdown(f"""
                        <div class="response-container success-animation">
                            <div class="response-header">
                                ✅ Performance Review Generated
                            </div>
                            <div class="response-content">
                                {response}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col2:
            st.info("""
            **💡 Review Tips:**
            
            • Be specific
            • Use examples
            • Balance feedback
            • Focus on behaviors
            • Set SMART goals
            """)
    
    with tab2:
        st.markdown("### SMART Goal Generator")
        
        goal_area = st.text_input("Goal Area", placeholder="e.g., Leadership Skills")
        
        if st.button("🎯 Generate Goals", use_container_width=True, type="primary"):
            if goal_area:
                with st.spinner("🤖 Creating SMART goals..."):
                    prompt = f"Generate 3-5 SMART goals for: {goal_area}"
                    response = call_openrouter_api(prompt)
                    
                    st.markdown(f"""
                    <div class="response-container success-animation">
                        <div class="response-header">
                            ✅ SMART Goals Generated
                        </div>
                        <div class="response-content">
                            {response}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

def show_training():
    """Training and development module"""
    st.markdown(f"## 🎓 Training & Development {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Build skills and grow your team")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📚 Learning Paths", "🎯 Skills Gap"])
    
    with tab1:
        st.markdown("### Create Learning Path")
        
        employee_role = st.text_input("Current Role", placeholder="e.g., Junior Developer")
        target_role = st.text_input("Target Role", placeholder="e.g., Senior Developer")
        timeline = st.selectbox("Timeline", ["3 months", "6 months", "1 year"])
        
        if st.button("🚀 Generate Path", use_container_width=True, type="primary"):
            if employee_role and target_role:
                with st.spinner("🤖 Creating learning path..."):
                    prompt = f"Create a learning path from {employee_role} to {target_role} in {timeline}"
                    response = call_openrouter_api(prompt)
                    
                    st.markdown(f"""
                    <div class="response-container success-animation">
                        <div class="response-header">
                            ✅ Learning Path Created
                        </div>
                        <div class="response-content">
                            {response}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Skills Gap Analysis")
        
        current_skills = st.text_area("Current Skills", height=100)
        required_skills = st.text_area("Required Skills", height=100)
        
        if st.button("🔍 Analyze Gap", use_container_width=True, type="primary"):
            if current_skills and required_skills:
                prompt = f"Analyze skills gap.\nCurrent: {current_skills}\nRequired: {required_skills}"
                response = call_openrouter_api(prompt)
                
                st.markdown(f"""
                <div class="response-container success-animation">
                    <div class="response-header">
                        ✅ Analysis Complete
                    </div>
                    <div class="response-content">
                        {response}
                    </div>
                </div>
                """, unsafe_allow_html=True)

def show_compensation():
    """Compensation module"""
    st.markdown(f"## 💰 Compensation {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Salary benchmarking and benefits")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Market Salary Analysis")
    
    job_title = st.text_input("Job Title", placeholder="e.g., Senior Engineer")
    location = st.text_input("Location", placeholder="e.g., San Francisco")
    experience = st.slider("Years of Experience", 0, 20, 5)
    
    if st.button("💰 Get Insights", use_container_width=True, type="primary"):
        if job_title:
            prompt = f"Salary benchmarking for {job_title} with {experience} years in {location}"
            response = call_openrouter_api(prompt)
            
            st.markdown(f"""
            <div class="response-container success-animation">
                <div class="response-header">
                    ✅ Salary Analysis
                </div>
                <div class="response-content">
                    {response}
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_leave():
    """Leave management"""
    st.markdown(f"## 📅 Leave Management {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Track and manage time off")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pending Requests", "8")
    with col2:
        st.metric("Approved This Month", "23")
    with col3:
        st.metric("Avg Days/Employee", "15.2")
    with col4:
        st.metric("Utilization Rate", "78%")

def show_offboarding():
    """Offboarding module"""
    st.markdown(f"## 🚪 Offboarding {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Smooth transitions for departing employees")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Generate Exit Checklist")
    
    employee_role = st.text_input("Role", placeholder="e.g., Marketing Manager")
    
    if st.button("📋 Generate Checklist", use_container_width=True, type="primary"):
        if employee_role:
            prompt = f"Create exit checklist for {employee_role}"
            response = call_openrouter_api(prompt)
            
            st.markdown(f"""
            <div class="response-container success-animation">
                <div class="response-header">
                    ✅ Exit Checklist
                </div>
                <div class="response-content">
                    {response}
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_analytics():
    """Analytics and reporting"""
    st.markdown(f"## 📊 Analytics {'<span class="demo-badge">DEMO MODE</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("Data-driven workforce insights")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Headcount", "1,234", "+5.2%")
    with col2:
        st.metric("Growth Rate", "12%", "+2%")
    with col3:
        st.metric("Avg Salary", "$95K", "+3.5%")
    with col4:
        st.metric("Satisfaction", "8.4/10", "+0.3")
    with col5:
        st.metric("Retention", "94%", "+2%")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("### 📄 Generate Report")
    
    report_type = st.selectbox("Report Type", [
        "Workforce Demographics",
        "Recruitment Metrics",
        "Performance Summary",
        "Compensation Analysis",
        "Turnover Report"
    ])
    
    time_period = st.selectbox("Period", ["Last Month", "Last Quarter", "Last Year"])
    
    if st.button("📊 Generate", use_container_width=True, type="primary"):
        prompt = f"Create a {report_type} report for {time_period}"
        response = call_openrouter_api(prompt)
        
        st.markdown(f"""
        <div class="response-container success-animation">
            <div class="response-header">
                ✅ Report Generated
            </div>
            <div class="response-content">
                {response}
            </div>
        </div>
        """, unsafe_allow_html=True)

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
    
    # Route to pages
    page_mapping = {
        "Dashboard": show_dashboard,
        "Recruitment": show_recruitment,
        "Onboarding": show_onboarding,
        "Employee Directory": show_employee_directory,
        "Performance Reviews": show_performance,
        "Training & Development": show_training,
        "Compensation": show_compensation,
        "Leave Management": show_leave,
        "Offboarding": show_offboarding,
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
    <p style="margin-top: 0.5rem;">Built with ❤️ by <strong>cybe4sent1nel(FAHAD KHAN)</strong></p>
    <p style="margin-top: 0.5rem;">🎮 Demo Mode Active - Explore all features with sample data</p>
</div>
""", unsafe_allow_html=True)

# Example: Department badge (replace or loop as needed)
for emp in st.session_state.employees:
    st.markdown(f"""
    <span style="background: #dbeafe; color: #1e40af; border-radius: 12px; font-size: 12px; font-weight: 600; padding: 0.25rem 0.75rem;">
        {emp['department']}
    </span>
    """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
