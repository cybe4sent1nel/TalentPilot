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
    page_title="TalentPilot - HR Management",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SVG Icons Library
SVG_ICONS = {
    "users": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>""",
    "briefcase": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"></path></svg>""",
    "target": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="12" r="5"></circle><circle cx="12" cy="12" r="9"></circle></svg>""",
    "bar-chart": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"></line><path d="M17 5H9.5a1.5 1.5 0 0 0-1.5 1.5v12a1.5 1.5 0 0 0 1.5 1.5H17"></path><path d="M3 12h4"></path></svg>""",
    "book": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>""",
    "dollar-sign": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a4 4 0 0 0 0 8h5a4 4 0 0 1 0 8H6"></path></svg>""",
    "calendar": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>""",
    "sign-out": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>""",
    "settings": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M12 1v6m0 6v6M4.22 4.22l4.24 4.24m3.08 3.08l4.24 4.24M1 12h6m6 0h6m-17.78 7.78l4.24-4.24m3.08-3.08l4.24-4.24"></path></svg>""",
    "search": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>""",
    "check": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>""",
    "plus": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>""",
    "bell": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>""",
    "trash": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>""",
    "edit": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>""",
    "arrow-right": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>""",
    "mail": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="M7 10l5 4 5-4"></path></svg>""",
    "phone": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>""",
    "home": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>""",
    "trending-up": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 17"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>""",
}

# Custom CSS for professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f9fafb;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f9fafb 100%);
        border-right: 1px solid #e5e7eb;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #1f2937;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1.5rem 1rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .logo-box {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }
    
    .logo-text {
        margin-left: 1rem;
        font-size: 22px;
        font-weight: 700;
        color: #1f2937;
        letter-spacing: -0.5px;
    }
    
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    
    .auth-container {
        max-width: 420px;
        margin: 3rem auto;
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
    }
    
    .auth-title {
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .auth-subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 2rem;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
    }
    
    .response-container {
        background: linear-gradient(135deg, #f0f9ff 0%, #f3f4f6 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        margin-top: 1.5rem;
    }
    
    .response-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        color: #1e40af;
        font-weight: 700;
        font-size: 16px;
    }
    
    .response-content {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        color: #374151;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    
    .activity-item {
        padding: 1rem;
        border-left: 3px solid #e5e7eb;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        background: white;
        border-radius: 8px;
    }
    
    .activity-item:hover {
        border-left-color: #3b82f6;
        background: #f9fafb;
    }
    
    .kanban-column {
        background: #f3f4f6;
        border-radius: 12px;
        padding: 1rem;
        min-height: 400px;
    }
    
    .kanban-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 3px solid #3b82f6;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        cursor: move;
        transition: all 0.3s ease;
    }
    
    .kanban-card:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .nav-item-active {
        background: #eff6ff !important;
        border-left: 3px solid #3b82f6 !important;
        color: #1e40af !important;
    }
    
    .metric-box {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 800;
        color: #1f2937;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 13px;
        color: #6b7280;
        font-weight: 500;
    }
    
    .metric-change {
        font-size: 12px;
        color: #10b981;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .badge-success {
        background: #dcfce7;
        color: #166534;
    }
    
    .badge-info {
        background: #dbeafe;
        color: #0c4a6e;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-danger {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .header-section {
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 28px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 14px;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

def svg_icon(name: str, size: int = 24, color: str = "currentColor") -> str:
    """Return SVG icon HTML"""
    if name in SVG_ICONS:
        svg = SVG_ICONS[name].replace('width="24"', f'width="{size}"').replace('height="24"', f'height="{size}"')
        if color != "currentColor":
            svg = svg.replace('currentColor', color)
        return svg
    return ""

# Initialize session state
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
        'user_name': 'Alex Johnson',
        'company_name': 'TechCorp Inc.',
        'employee_count': 1234,
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
            'applied_date': '2024-01-21',
            'interview_date': '2024-02-08'
        }
    ]

def generate_notifications():
    return [
        {'id': 1, 'type': 'urgent', 'message': '3 interviews scheduled for today', 'time': '2 hours ago', 'read': False},
        {'id': 2, 'type': 'info', 'message': 'New performance review templates available', 'time': '5 hours ago', 'read': False},
        {'id': 3, 'type': 'success', 'message': '5 new job applications received', 'time': '1 day ago', 'read': True},
    ]

def generate_tasks():
    return [
        {'id': 1, 'title': 'Review Sarah Johnson\'s performance', 'priority': 'High', 'due': '2024-02-10', 'status': 'In Progress'},
        {'id': 2, 'title': 'Schedule interviews for PM role', 'priority': 'High', 'due': '2024-02-08', 'status': 'To Do'},
        {'id': 3, 'title': 'Update employee handbook', 'priority': 'Medium', 'due': '2024-02-15', 'status': 'To Do'},
        {'id': 4, 'title': 'Process Q1 bonuses', 'priority': 'High', 'due': '2024-02-20', 'status': 'To Do'},
    ]

# API Call Function
def call_openrouter_api(prompt, system_message="You are TalentPilot, an expert HR AI assistant. Provide professional, detailed HR advice."):
    """Call OpenRouter API"""
    if st.session_state.demo_mode:
        time.sleep(1.5)
        
        if 'job description' in prompt.lower():
            return """Senior Software Engineer

Job Summary:
We are seeking an experienced Senior Software Engineer to join our dynamic technology team.

Key Responsibilities:
• Design and develop scalable web applications
• Lead technical discussions and architectural decisions
• Collaborate with cross-functional teams
• Mentor junior developers through code reviews
• Write clean, maintainable code following best practices

Required Qualifications:
• 5+ years of professional software development
• Strong proficiency in JavaScript/TypeScript and React
• Experience with RESTful APIs and microservices
• Understanding of database design
• Experience with cloud platforms
• Bachelor's degree in Computer Science

Preferred Qualifications:
• Experience with Docker and Kubernetes
• Knowledge of DevOps practices and CI/CD
• Contributions to open-source projects

What We Offer:
• Competitive salary: $120,000 - $160,000
• Equity compensation
• Comprehensive health insurance
• 401(k) matching up to 6%
• Flexible work arrangements
• Professional development budget"""
        
        return "Demo response for: " + prompt
    
    try:
        headers = {
            'Authorization': f'Bearer {st.session_state.api_key}',
            'Content-Type': 'application/json',
        }
        
        data = {
            'model': 'openai/gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 1500
        }
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code}"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Authentication Page
def show_auth_page():
    """Display authentication page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="auth-container">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div class="logo-box" style="margin: 0 auto; width: 64px; height: 64px; font-size: 32px;">TP</div>
            </div>
            <h1 class="auth-title">TalentPilot</h1>
            <p class="auth-subtitle">AI-Powered HR Management System</p>
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
            if st.button("Connect", use_container_width=True, type="primary"):
                if api_key:
                    st.session_state.api_key = api_key
                    st.session_state.authenticated = True
                    st.session_state.demo_mode = False
                    st.success("Connected successfully")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Please enter your API key")
        
        with col_btn2:
            if st.button("Demo Mode", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.demo_mode = True
                st.success("Demo mode activated")
                time.sleep(1)
                st.rerun()

# Sidebar Navigation
def show_sidebar():
    """Display sidebar navigation"""
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="logo-container">
            <div class="logo-box">TP</div>
            <div class="logo-text">TalentPilot</div>
        </div>
        """, unsafe_allow_html=True)
        
        # User Info
        st.markdown(f"""
        <div style="background: #f3f4f6; border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem;">
            <div style="font-weight: 600; color: #1f2937;">{st.session_state.user_name}</div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 0.25rem;">{st.session_state.company_name}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Demo Mode Badge
        if st.session_state.demo_mode:
            st.info("Demo Mode - Sample data only")
        
        # Navigation Menu
        st.markdown("### Navigation")
        
        pages = {
            "Dashboard": "Dashboard",
            "Employees": "Employee Directory",
            "Recruitment": "Recruitment",
            "Tasks": "Tasks",
            "AI Assistant": "AI Assistant"
        }
        
        for label, page in pages.items():
            is_active = st.session_state.current_page == page
            if st.button(
                f"• {label}", 
                use_container_width=True, 
                key=page,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### Overview")
        st.metric("Total Employees", st.session_state.employee_count)
        st.metric("Open Positions", len(st.session_state.job_postings))
        st.metric("Pending Tasks", len([t for t in st.session_state.tasks if t['status'] != 'Done']))
        
        st.markdown("---")
        
        # Logout
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.api_key = ''
            st.rerun()

# Dashboard Page
def show_dashboard():
    """Display dashboard"""
    st.markdown("""
    <div class="header-section">
        <div class="header-title">Welcome back, Alex</div>
        <div class="header-subtitle">Here's your HR dashboard for today</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("Total Employees", "1,234", "+12%"),
        ("Open Positions", "23", "+5 this week"),
        ("Pending Reviews", "45", "15 due"),
        ("Training Progress", "78%", "+8%"),
        ("Satisfaction", "8.4/10", "+0.3")
    ]
    
    for col, (label, value, change) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-change">{change}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Content
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### Recent Activity")
        
        activities = [
            ("New hire onboarded", "Sarah Johnson - Software Engineer", "2 hours ago"),
            ("Interview scheduled", "Michael Chen - Product Manager", "5 hours ago"),
            ("Performance review completed", "Emily Davis - Sales Director", "1 day ago"),
            ("Leave request pending", "James Wilson - 3 days vacation", "2 days ago"),
        ]
        
        for title, desc, time_ago in activities:
            st.markdown(f"""
            <div class="activity-item">
                <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">{title}</div>
                <div style="font-size: 13px; color: #6b7280; margin-bottom: 0.25rem;">{desc}</div>
                <div style="font-size: 12px; color: #9ca3af;">{time_ago}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("### Quick Actions")
        
        if st.button("Post New Job", use_container_width=True):
            st.session_state.current_page = "Recruitment"
            st.rerun()
        
        if st.button("Add Employee", use_container_width=True):
            st.session_state.current_page = "Employee Directory"
            st.rerun()
        
        if st.button("Create Task", use_container_width=True):
            st.session_state.current_page = "Tasks"
            st.rerun()
        
        if st.button("Ask AI", use_container_width=True):
            st.session_state.current_page = "AI Assistant"
            st.rerun()

# Employee Directory
def show_employee_directory():
    """Display employee directory"""
    st.markdown("""
    <div class="header-section">
        <div class="header-title">Employee Directory</div>
        <div class="header-subtitle">Manage all employee information</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and Filters
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search = st.text_input("Search employees", placeholder="Name, role, department...")
    
    with col2:
        dept = st.selectbox("Department", ["All"] + list(set([e['department'] for e in st.session_state.employees])))
    
    with col3:
        status = st.selectbox("Status", ["All", "Active", "On Leave"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display employees
    for emp in st.session_state.employees:
        with st.container():
            st.markdown(f"""
            <div class="feature-card">
                <div style="display: flex; gap: 1.5rem;">
                    <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #3b82f6, #1e40af); 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                color: white; font-weight: 700; font-size: 20px;">
                        {emp['name'][0]}{emp['name'].split()[-1][0]}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 700; color: #1f2937; font-size: 18px;">{emp['name']}</div>
                        <div style="color: #3b82f6; font-weight: 600; margin-bottom: 0.5rem;">{emp['role']}</div>
                        <div style="display: flex; gap: 1rem; font-size: 13px; color: #6b7280;">
                            <span>{emp['department']}</span>
                            <span>{emp['email']}</span>
                            <span>{emp['location']}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge badge-success">{emp['status']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("View Profile", key=f"view_{emp['id']}", use_container_width=True)
            with col2:
                st.button("Edit", key=f"edit_{emp['id']}", use_container_width=True)
            with col3:
                st.button("Contact", key=f"contact_{emp['id']}", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

# Recruitment Page
def show_recruitment():
    """Display recruitment module"""
    st.markdown("""
    <div class="header-section">
        <div class="header-title">Recruitment Hub</div>
        <div class="header-subtitle">Manage job postings and candidates</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recruitment Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""<div class="metric-box"><div class="metric-label">Open Positions</div>
        <div class="metric-value">23</div></div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="metric-box"><div class="metric-label">Applications</div>
        <div class="metric-value">145</div></div>""", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""<div class="metric-box"><div class="metric-label">In Interview</div>
        <div class="metric-value">18</div></div>""", unsafe_allow_html=True)
    
    with col4:
        st.markdown("""<div class="metric-box"><div class="metric-label">Avg Time to Hire</div>
        <div class="metric-value">28d</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Job Postings", "Candidates", "AI Tools"])
    
    with tab1:
        st.markdown("### Active Job Postings")
        
        for job in st.session_state.job_postings:
            st.markdown(f"""
            <div class="feature-card">
                <div style="display: flex; justify-content: space-between;">
                    <div style="flex: 1;">
                        <div style="font-weight: 700; color: #1f2937; font-size: 18px;">{job['title']}</div>
                        <div style="display: flex; gap: 1rem; font-size: 13px; color: #6b7280; margin-top: 0.5rem;">
                            <span>{job['location']}</span>
                            <span>{job['type']}</span>
                            <span>{job['salary_range']}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 700; color: #3b82f6; font-size: 24px;">{job['applications']}</div>
                        <div style="font-size: 12px; color: #6b7280;">applications</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("View Details", key=f"job_{job['id']}", use_container_width=True)
            with col2:
                st.button("Edit", key=f"edit_job_{job['id']}", use_container_width=True)
            with col3:
                st.button("View Applicants", key=f"applicants_{job['id']}", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Candidates")
        
        for candidate in st.session_state.candidates:
            st.markdown(f"""
            <div class="feature-card">
                <div style="display: flex; gap: 1.5rem; justify-content: space-between;">
                    <div style="flex: 1;">
                        <div style="font-weight: 700; color: #1f2937; font-size: 18px;">{candidate['name']}</div>
                        <div style="color: #6b7280; margin-top: 0.25rem;">{candidate['position_applied']}</div>
                        <div style="display: flex; gap: 1rem; font-size: 12px; color: #6b7280; margin-top: 0.5rem;">
                            <span>{candidate['email']}</span>
                            <span>{candidate['experience']}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 700; color: #10b981; font-size: 24px;">{candidate['score']}</div>
                        <div style="font-size: 12px; color: #6b7280;">AI Score</div>
                        <span class="badge badge-warning" style="margin-top: 0.5rem;">{candidate['status']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("View Resume", key=f"resume_{candidate['id']}", use_container_width=True)
            with col2:
                st.button("Schedule Interview", key=f"interview_{candidate['id']}", use_container_width=True)
            with col3:
                st.button("Send Email", key=f"email_{candidate['id']}", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### AI-Powered Tools")
        
        sub_tab1, sub_tab2 = st.tabs(["Job Description", "Resume Analyzer"])
        
        with sub_tab1:
            job_input = st.text_area("Job Details", placeholder="Senior Software Engineer with 5+ years in React...")
            
            if st.button("Generate Description", use_container_width=True, type="primary"):
                if job_input:
                    with st.spinner("Generating..."):
                        response = call_openrouter_api(f"Generate job description for: {job_input}")
                        st.markdown(f"""<div class="response-container">
                        <div class="response-header">Generated Job Description</div>
                        <div class="response-content">{response}</div>
                        </div>""", unsafe_allow_html=True)
        
        with sub_tab2:
            resume_text = st.text_area("Resume Content", placeholder="Paste resume text...")
            
            if st.button("Analyze Resume", use_container_width=True, type="primary"):
                if resume_text:
                    with st.spinner("Analyzing..."):
                        response = call_openrouter_api(f"Analyze this resume: {resume_text}")
                        st.markdown(f"""<div class="response-container">
                        <div class="response-header">Analysis Results</div>
                        <div class="response-content">{response}</div>
                        </div>""", unsafe_allow_html=True)

# Tasks Page
def show_tasks():
    """Display tasks"""
    st.markdown("""
    <div class="header-section">
        <div class="header-title">Task Management</div>
        <div class="header-subtitle">Track and manage your tasks</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Task Stats
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(st.session_state.tasks)
    completed = len([t for t in st.session_state.tasks if t['status'] == 'Done'])
    high = len([t for t in st.session_state.tasks if t['priority'] == 'High'])
    
    st.metric("Total Tasks", total, col=col1)
    st.metric("Completed", completed, col=col2)
    st.metric("High Priority", high, col=col3)
    st.metric("Completion", f"{int(completed/total*100)}%", col=col4)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Task Kanban
    col1, col2, col3, col4 = st.columns(4)
    
    statuses = ["To Do", "In Progress", "Planning", "Done"]
    
    for col, status in zip([col1, col2, col3, col4], statuses):
        with col:
            st.markdown(f"### {status}")
            tasks = [t for t in st.session_state.tasks if t['status'] == status]
            
            for task in tasks:
                priority_color = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#3b82f6"}[task['priority']]
                
                st.markdown(f"""
                <div class="kanban-card" style="border-left-color: {priority_color};">
                    <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">{task['title']}</div>
                    <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span class="badge" style="background: {priority_color}20; color: {priority_color};">
                            {task['priority']}
                        </span>
                    </div>
                    <div style="font-size: 12px; color: #6b7280;">Due: {task['due']}</div>
                </div>
                """, unsafe_allow_html=True)

# AI Assistant Page
def show_ai_assistant():
    """Display AI assistant"""
    st.markdown("""
    <div class="header-section">
        <div class="header-title">AI Assistant</div>
        <div class="header-subtitle">Your intelligent HR co-pilot</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick prompts
    st.markdown("### Quick Prompts")
    
    prompts = [
        "Generate a job description for a Data Scientist",
        "Create an onboarding plan for a Marketing Manager",
        "Help me design a compensation package",
        "Write performance review questions",
    ]
    
    cols = st.columns(2)
    for idx, prompt in enumerate(prompts):
        col = cols[idx % 2]
        with col:
            if st.button(prompt, use_container_width=True, key=f"prompt_{idx}"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                response = call_openrouter_api(prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat history
    if st.session_state.chat_history:
        st.markdown("### Conversation")
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                    <div style="background: #3b82f6; color: white; padding: 1rem; border-radius: 12px; max-width: 70%;">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                    <div style="background: #f3f4f6; color: #1f2937; padding: 1rem; border-radius: 12px; max-width: 80%;">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Ask anything...", placeholder="Type your question...", label_visibility="collapsed")
    with col2:
        send = st.button("Send", type="primary", use_container_width=True)
    
    if send and user_input:
        with st.spinner("Thinking..."):
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            response = call_openrouter_api(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

# Main Application
def main():
    """Main application"""
    init_session_state()
    
    if not st.session_state.authenticated:
        show_auth_page()
        return
    
    show_sidebar()
    
    # Route pages
    if st.session_state.current_page == "Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "Employee Directory":
        show_employee_directory()
    elif st.session_state.current_page == "Recruitment":
        show_recruitment()
    elif st.session_state.current_page == "Tasks":
        show_tasks()
    elif st.session_state.current_page == "AI Assistant":
        show_ai_assistant()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 13px; padding: 1rem;">
        <p><strong>TalentPilot</strong> - AI-Powered HR Management</p>
        <p style="margin-top: 0.5rem; font-size: 12px;">Built with professional design standards</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
