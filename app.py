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

# IBM Design System CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&display=swap');
    
    * {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        background-color: #f4f4f4;
    }
    
    /* IBM Header Styles */
    .ibm-header {
        background: #000000;
        padding: 1rem 2rem;
        border-bottom: 1px solid #393939;
    }
    
    .ibm-header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 99rem;
        margin: 0 auto;
    }
    
    .ibm-logo {
        color: #ffffff;
        font-weight: 600;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* IBM Button Styles */
    .stButton > button {
        background-color: #0f62fe;
        color: white;
        border: none;
        border-radius: 0;
        padding: 0.75rem 1rem;
        font-weight: 400;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        min-height: 3rem;
    }
    
    .stButton > button:hover {
        background-color: #0353e9;
        color: white;
    }
    
    .stButton > button:focus {
        box-shadow: inset 0 0 0 2px #0f62fe, inset 0 0 0 3px white;
    }
    
    /* IBM Secondary Button */
    .ibm-btn--secondary {
        background-color: #393939 !important;
        color: white !important;
    }
    
    .ibm-btn--secondary:hover {
        background-color: #4c4c4c !important;
    }
    
    /* IBM Tertiary Button */
    .ibm-btn--tertiary {
        background-color: transparent !important;
        color: #0f62fe !important;
        border: 1px solid #0f62fe !important;
    }
    
    .ibm-btn--tertiary:hover {
        background-color: #f4f4f4 !important;
    }
    
    /* IBM Card Styles */
    .ibm-card {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .ibm-card--interactive {
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .ibm-card--interactive:hover {
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        border-color: #0f62fe;
    }
    
    /* IBM Grid System */
    .ibm-grid {
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        gap: 2rem;
        max-width: 99rem;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .ibm-col-1 { grid-column: span 1; }
    .ibm-col-2 { grid-column: span 2; }
    .ibm-col-3 { grid-column: span 3; }
    .ibm-col-4 { grid-column: span 4; }
    .ibm-col-6 { grid-column: span 6; }
    .ibm-col-8 { grid-column: span 8; }
    .ibm-col-9 { grid-column: span 9; }
    .ibm-col-12 { grid-column: span 12; }
    
    /* IBM Typography */
    .ibm-type-alpha {
        font-size: 2.625rem;
        font-weight: 300;
        line-height: 1.19;
        letter-spacing: 0;
    }
    
    .ibm-type-beta {
        font-size: 2rem;
        font-weight: 300;
        line-height: 1.25;
        letter-spacing: 0;
    }
    
    .ibm-type-gamma {
        font-size: 1.75rem;
        font-weight: 400;
        line-height: 1.29;
        letter-spacing: 0;
    }
    
    .ibm-type-delta {
        font-size: 1.25rem;
        font-weight: 400;
        line-height: 1.4;
        letter-spacing: 0;
    }
    
    .ibm-type-epsilon {
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.5;
        letter-spacing: 0;
    }
    
    .ibm-type-zeta {
        font-size: 0.875rem;
        font-weight: 400;
        line-height: 1.43;
        letter-spacing: 0.16px;
    }
    
    .ibm-type-caption {
        font-size: 0.75rem;
        font-weight: 400;
        line-height: 1.33;
        letter-spacing: 0.32px;
    }
    
    /* IBM Colors */
    .ibm-color-blue-60 { color: #0f62fe; }
    .ibm-color-gray-100 { color: #f4f4f4; }
    .ibm-color-gray-80 { color: #393939; }
    .ibm-color-gray-70 { color: #525252; }
    .ibm-color-gray-60 { color: #6f6f6f; }
    
    /* IBM Sidebar */
    [data-testid="stSidebar"] {
        background: #f4f4f4;
        border-right: 1px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #161616;
    }
    
    /* IBM Form Elements */
    .stTextInput > div > div > input {
        border-radius: 0;
        border: 1px solid #8d8d8d;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
    }
    
    .stTextInput > div > div > input:focus {
        outline: 2px solid #0f62fe;
        outline-offset: -2px;
    }
    
    .stSelectbox > div > div > div {
        border-radius: 0;
        border: 1px solid #8d8d8d;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 0;
        border: 1px solid #8d8d8d;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
    }
    
    /* IBM Dataframe Styling */
    .dataframe {
        border: 1px solid #e0e0e0;
    }
    
    .dataframe th {
        background: #f4f4f4;
        color: #161616;
        font-weight: 600;
        border: 1px solid #e0e0e0;
    }
    
    .dataframe td {
        border: 1px solid #e0e0e0;
    }
    
    /* IBM Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #f4f4f4;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f4f4f4;
        border-radius: 0;
        padding: 1rem 1.5rem;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        border-bottom: 2px solid #0f62fe;
        color: #0f62fe;
    }
    
    /* IBM Metric Cards */
    .ibm-metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 1.5rem;
        text-align: center;
    }
    
    .ibm-metric-value {
        font-size: 2.625rem;
        font-weight: 300;
        color: #161616;
        line-height: 1.19;
    }
    
    .ibm-metric-label {
        font-size: 0.875rem;
        color: #525252;
        margin-top: 0.5rem;
    }
    
    /* IBM Status Indicators */
    .ibm-status--active {
        color: #24a148;
        font-weight: 600;
    }
    
    .ibm-status--pending {
        color: #f1c21b;
        font-weight: 600;
    }
    
    .ibm-status--inactive {
        color: #da1e28;
        font-weight: 600;
    }
    
    /* IBM Tag Styles */
    .ibm-tag {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        background: #e0e0e0;
        color: #161616;
        font-size: 0.75rem;
        font-weight: 400;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .ibm-tag--blue {
        background: #edf5ff;
        color: #0043ce;
    }
    
    .ibm-tag--green {
        background: #defbe6;
        color: #0e6027;
    }
    
    /* Custom IBM Components */
    .ibm-page-header {
        background: white;
        padding: 2rem;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    .ibm-content-section {
        background: white;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #e0e0e0;
    }
    
    .ibm-divider {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 2rem 0;
    }
    
    /* Demo Badge */
    .demo-badge {
        display: inline-block;
        background: #f1c21b;
        color: #161616;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

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

# Generate sample data (same as before)
def generate_sample_employees():
    return [
        {
            'id': 'EMP001', 'name': 'Sarah Johnson', 'role': 'Senior Software Engineer', 'department': 'Engineering',
            'email': 'sarah.j@company.com', 'phone': '+1 (555) 123-4567', 'hire_date': '2021-03-15', 'salary': 125000,
            'status': 'Active', 'manager': 'John Smith', 'location': 'San Francisco, CA',
            'skills': ['Python', 'React', 'AWS', 'Docker'], 'performance_score': 4.5, 'pto_balance': 15
        },
        {
            'id': 'EMP002', 'name': 'Michael Chen', 'role': 'Marketing Manager', 'department': 'Marketing',
            'email': 'michael.c@company.com', 'phone': '+1 (555) 234-5678', 'hire_date': '2020-07-20', 'salary': 95000,
            'status': 'Active', 'manager': 'Lisa Wong', 'location': 'New York, NY',
            'skills': ['SEO', 'Content Strategy', 'Analytics', 'Social Media'], 'performance_score': 4.2, 'pto_balance': 12
        }
    ]

def generate_sample_jobs():
    return [
        {
            'id': 'JOB001', 'title': 'Senior Full-Stack Developer', 'department': 'Engineering', 'location': 'Remote',
            'type': 'Full-time', 'salary_range': '$120k - $160k', 'posted_date': '2024-01-15', 'applications': 45,
            'status': 'Open', 'description': 'Looking for an experienced full-stack developer...'
        }
    ]

def generate_sample_candidates():
    return [
        {
            'id': 'CAN001', 'name': 'Alex Thompson', 'email': 'alex.t@email.com', 'phone': '+1 (555) 111-2222',
            'position_applied': 'Senior Full-Stack Developer', 'status': 'Phone Screen', 'score': 85,
            'experience': '7 years', 'education': 'BS Computer Science', 'skills': ['React', 'Node.js', 'PostgreSQL', 'AWS'],
            'resume_url': 'resumes/alex_thompson.pdf', 'applied_date': '2024-01-16', 'interview_date': '2024-02-05'
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
        {'id': 'TEMP001', 'name': 'Standard Professional Offer', 'description': 'Comprehensive professional offer letter', 'category': 'Professional'},
        {'id': 'TEMP002', 'name': 'Executive Offer Package', 'description': 'Detailed executive offer with equity', 'category': 'Executive'},
        {'id': 'TEMP003', 'name': 'Internship Offer', 'description': 'Simple internship offer letter', 'category': 'Internship'}
    ]

# AI API Call Function (same as before)
def call_openrouter_api(prompt, system_message="You are TalentPilot, an expert HR AI assistant powered by IBM Watsonx. Provide professional, detailed, and actionable HR advice and content. When asked about developers, owners, or founders, mention that the system was developed by FAHAD KHAN."):
    if st.session_state.demo_mode:
        time.sleep(1.5)
        if any(keyword in prompt.lower() for keyword in ['developer', 'owner', 'founder', 'created', 'built', 'fahad', 'khan']):
            return """**About TalentPilot**

**Developer & Founder:** FAHAD KHAN

TalentPilot was conceptualized, designed, and developed by **FAHAD KHAN**, an experienced professional in HR technology and AI systems.

**Key Achievements:**
- Designed end-to-end HR orchestration platform
- Integrated advanced AI capabilities using IBM Watsonx
- Created comprehensive feature set covering entire employee lifecycle
- Built scalable architecture for enterprise HR operations

**Vision:** To make HR processes more efficient, data-driven, and employee-centric through cutting-edge technology.

For any inquiries about TalentPilot's development or future roadmap, please contact FAHAD KHAN."""
        # ... other demo responses remain the same
        else:
            return """**TalentPilot AI Assistant**

**Powered by IBM Watsonx**

Hello! I'm your AI-powered HR co-pilot, enhanced with IBM Watsonx capabilities. I can help you with HR tasks including recruitment, employee management, and offer letter generation.

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

# IBM Header Component
def show_ibm_header():
    st.markdown("""
    <div class="ibm-header">
        <div class="ibm-header-content">
            <div class="ibm-logo">
                <span>TalentPilot</span>
                <span class="ibm-type-zeta" style="color: #a2a9b0;">| AI HR Orchestration</span>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span class="ibm-type-zeta" style="color: #ffffff;">{}</span>
                <span class="ibm-type-zeta" style="color: #a2a9b0;">{}</span>
            </div>
        </div>
    </div>
    """.format(st.session_state.user_name, st.session_state.company_name), unsafe_allow_html=True)

# IBM Sidebar
def show_ibm_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 2rem 1rem;">
            <div class="ibm-type-delta" style="margin-bottom: 2rem; color: #161616;">HR Management</div>
        """, unsafe_allow_html=True)
        
        # Navigation
        pages = {
            "Dashboard": "Dashboard",
            "Recruitment": "Recruitment",
            "Employee Directory": "Employee Directory", 
            "Performance Reviews": "Performance Reviews",
            "Offer Letters": "Offer Letters",
            "Training & Development": "Training & Development",
            "Compensation": "Compensation",
            "Analytics": "Analytics",
            "AI Assistant": "AI Assistant"
        }
        
        for label, page in pages.items():
            is_active = st.session_state.current_page == page
            button_style = "" if is_active else "ibm-btn--tertiary"
            
            if st.button(
                label,
                use_container_width=True,
                key=page,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# IBM Dashboard
def show_dashboard():
    show_ibm_header()
    
    st.markdown("""
    <div class="ibm-page-header">
        <h1 class="ibm-type-alpha">HR Dashboard</h1>
        <p class="ibm-type-epsilon" style="color: #525252;">Overview of your HR operations and key metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown('<div class="ibm-grid">', unsafe_allow_html=True)
    
    metrics = [
        {"value": "1,234", "label": "Total Employees", "change": "+12%"},
        {"value": "23", "label": "Open Positions", "change": "+5"},
        {"value": "45", "label": "Pending Reviews", "change": "15 due"},
        {"value": "78%", "label": "Training Progress", "change": "+8%"}
    ]
    
    for metric in metrics:
        st.markdown(f"""
        <div class="ibm-col-3">
            <div class="ibm-metric-card">
                <div class="ibm-metric-value">{metric['value']}</div>
                <div class="ibm-metric-label">{metric['label']}</div>
                <div class="ibm-type-caption" style="color: #0f62fe; margin-top: 0.5rem;">{metric['change']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("""
    <div class="ibm-content-section">
        <h2 class="ibm-type-gamma">Recent Activity</h2>
        <div class="ibm-divider"></div>
    """, unsafe_allow_html=True)
    
    activities = [
        {"action": "New hire onboarded", "details": "Sarah Johnson - Software Engineer", "time": "2 hours ago"},
        {"action": "Interview scheduled", "details": "Michael Chen - Product Manager", "time": "5 hours ago"},
        {"action": "Performance review completed", "details": "Emily Davis - Sales Director", "time": "1 day ago"}
    ]
    
    for activity in activities:
        st.markdown(f"""
        <div class="ibm-card">
            <div style="display: flex; justify-content: between; align-items: start;">
                <div style="flex: 1;">
                    <div class="ibm-type-delta" style="margin-bottom: 0.5rem;">{activity['action']}</div>
                    <div class="ibm-type-zeta" style="color: #525252;">{activity['details']}</div>
                </div>
                <div class="ibm-type-caption" style="color: #6f6f6f;">{activity['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# IBM Employee Directory
def show_employee_directory():
    show_ibm_header()
    
    st.markdown("""
    <div class="ibm-page-header">
        <h1 class="ibm-type-alpha">Employee Directory</h1>
        <p class="ibm-type-epsilon" style="color: #525252;">Manage and view all employee information</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.text_input("Search employees", placeholder="Name, role, department...")
    with col2:
        st.selectbox("Department", ["All", "Engineering", "Marketing", "Sales", "HR"])
    with col3:
        st.selectbox("Status", ["All", "Active", "On Leave"])
    
    st.markdown("""
    <div class="ibm-content-section">
        <h2 class="ibm-type-gamma">Employees</h2>
        <div class="ibm-divider"></div>
    """, unsafe_allow_html=True)
    
    for emp in st.session_state.employees:
        st.markdown(f"""
        <div class="ibm-card ibm-card--interactive">
            <div style="display: flex; align-items: start; gap: 1.5rem;">
                <div style="width: 64px; height: 64px; background: #0f62fe; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600;">
                    {emp['name'][0]}
                </div>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 1rem;">
                        <div>
                            <div class="ibm-type-delta" style="margin-bottom: 0.25rem;">{emp['name']}</div>
                            <div class="ibm-type-zeta" style="color: #0f62fe;">{emp['role']}</div>
                        </div>
                        <div class="ibm-status--active">Active</div>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem;">
                        <div>
                            <div class="ibm-type-caption" style="color: #6f6f6f;">Department</div>
                            <div class="ibm-type-zeta">{emp['department']}</div>
                        </div>
                        <div>
                            <div class="ibm-type-caption" style="color: #6f6f6f;">Location</div>
                            <div class="ibm-type-zeta">{emp['location']}</div>
                        </div>
                    </div>
                    <div>
                        <div class="ibm-type-caption" style="color: #6f6f6f; margin-bottom: 0.5rem;">Skills</div>
                        <div>
                            {' '.join([f'<span class="ibm-tag">{skill}</span>' for skill in emp['skills'][:3]])}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# IBM Recruitment Page
def show_recruitment():
    show_ibm_header()
    
    st.markdown("""
    <div class="ibm-page-header">
        <h1 class="ibm-type-alpha">Recruitment Hub</h1>
        <p class="ibm-type-epsilon" style="color: #525252;">AI-powered hiring and candidate management</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Job Postings", "Candidates", "AI Tools"])
    
    with tab1:
        st.markdown("""
        <div class="ibm-content-section">
            <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 2rem;">
                <h2 class="ibm-type-gamma">Active Job Postings</h2>
                <button class="stButton" style="display: inline-block;">
                    <button>Create New Job</button>
                </button>
            </div>
        """, unsafe_allow_html=True)
        
        for job in st.session_state.job_postings:
            st.markdown(f"""
            <div class="ibm-card ibm-card--interactive">
                <div style="display: flex; justify-content: between; align-items: start;">
                    <div style="flex: 1;">
                        <div class="ibm-type-delta" style="margin-bottom: 0.5rem;">{job['title']}</div>
                        <div style="display: flex; gap: 2rem; margin-bottom: 1rem;">
                            <div>
                                <div class="ibm-type-caption" style="color: #6f6f6f;">Location</div>
                                <div class="ibm-type-zeta">{job['location']}</div>
                            </div>
                            <div>
                                <div class="ibm-type-caption" style="color: #6f6f6f;">Applications</div>
                                <div class="ibm-type-zeta">{job['applications']}</div>
                            </div>
                            <div>
                                <div class="ibm-type-caption" style="color: #6f6f6f;">Status</div>
                                <div class="ibm-type-zeta ibm-status--active">{job['status']}</div>
                            </div>
                        </div>
                        <div class="ibm-type-zeta" style="color: #525252;">{job['description'][:100]}...</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# IBM Offer Letters Page
def show_offer_letters():
    show_ibm_header()
    
    st.markdown("""
    <div class="ibm-page-header">
        <h1 class="ibm-type-alpha">Offer Letters</h1>
        <p class="ibm-type-epsilon" style="color: #525252;">Generate professional offer letters with AI-powered templates</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Generate Offer", "Templates", "Custom Templates"])
    
    with tab1:
        st.markdown("""
        <div class="ibm-content-section">
            <h2 class="ibm-type-gamma">Generate New Offer Letter</h2>
            <div class="ibm-divider"></div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            candidate_name = st.text_input("Candidate Name")
            position = st.text_input("Position")
            department = st.selectbox("Department", ["Engineering", "Marketing", "Sales", "HR", "Finance"])
        with col2:
            offer_type = st.selectbox("Offer Type", ["Full-time", "Contract", "Internship", "Executive"])
            base_salary = st.number_input("Base Salary ($)", value=100000)
            start_date = st.date_input("Start Date")
        
        if st.button("Generate Offer Letter", type="primary"):
            if candidate_name and position:
                with st.spinner("Generating offer letter..."):
                    prompt = f"Generate a professional {offer_type} offer letter for {candidate_name} for {position} position in {department} department. Base salary: ${base_salary:,}. Start date: {start_date}."
                    response = call_openrouter_api(prompt)
                    
                    st.markdown("""
                    <div class="ibm-content-section">
                        <h3 class="ibm-type-delta">Generated Offer Letter</h3>
                        <div class="ibm-divider"></div>
                        <div style="background: #f4f4f4; padding: 2rem; border: 1px solid #e0e0e0;">
                    """, unsafe_allow_html=True)
                    st.markdown(response)
                    st.markdown("</div></div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="ibm-content-section">
            <h2 class="ibm-type-gamma">Offer Letter Templates</h2>
            <div class="ibm-divider"></div>
        """, unsafe_allow_html=True)
        
        for template in st.session_state.offer_templates:
            st.markdown(f"""
            <div class="ibm-card ibm-card--interactive">
                <div class="ibm-type-delta" style="margin-bottom: 0.5rem;">{template['name']}</div>
                <div class="ibm-type-zeta" style="color: #525252; margin-bottom: 1rem;">{template['description']}</div>
                <span class="ibm-tag ibm-tag--blue">{template['category']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# IBM AI Assistant Page
def show_ai_assistant():
    show_ibm_header()
    
    st.markdown("""
    <div class="ibm-page-header">
        <h1 class="ibm-type-alpha">AI Assistant</h1>
        <p class="ibm-type-epsilon" style="color: #525252;">Your intelligent HR co-pilot powered by IBM Watsonx</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="ibm-content-section">
        <div style="background: #f4f4f4; padding: 2rem; border: 1px solid #e0e0e0; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="width: 40px; height: 40px; background: #0f62fe; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600;">AI</div>
                <div>
                    <div class="ibm-type-delta">TalentPilot AI Assistant</div>
                    <div class="ibm-type-zeta" style="color: #525252;">Powered by IBM Watsonx</div>
                </div>
            </div>
            <div class="ibm-type-epsilon">
                Hello! I'm your AI-powered HR co-pilot. I can help you with recruitment, employee management, 
                offer letter generation, and other HR tasks. How can I assist you today?
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Suggested prompts
    st.markdown("""
    <h3 class="ibm-type-delta">Try these prompts:</h3>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 2rem;">
    """, unsafe_allow_html=True)
    
    prompts = [
        "Generate a job description for a Data Scientist",
        "Create an onboarding plan for a new Marketing Manager",
        "Help me design a compensation package for senior engineers",
        "Who developed this TalentPilot system?"
    ]
    
    for prompt in prompts:
        if st.button(prompt, use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            response = call_openrouter_api(prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat history
    if st.session_state.chat_history:
        st.markdown("<h3 class='ibm-type-delta'>Conversation</h3>", unsafe_allow_html=True)
        for message in st.session_state.chat_history[-6:]:  # Show last 6 messages
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                    <div style="background: #0f62fe; color: white; padding: 1rem; max-width: 70%;">
                        <div class="ibm-type-epsilon">{message['content']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                    <div style="background: #f4f4f4; padding: 1rem; max-width: 80%; border: 1px solid #e0e0e0;">
                        <div class="ibm-type-epsilon">{message['content']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Placeholder functions for other pages
def show_performance():
    show_ibm_header()
    st.markdown("""
    <div class="ibm-page-header">
        <h1 class="ibm-type-alpha">Performance Reviews</h1>
        <p class="ibm-type-epsilon" style="color: #525252;">360-degree feedback and goal tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Performance Reviews module - Enhanced with IBM Watsonx")

def show_training():
    show_ibm_header()
    st.markdown("""
    <div class="ibm-page-header">
        <h1 class="ibm-type-alpha">Training & Development</h1>
        <p class="ibm-type-epsilon" style="color: #525252;">Build skills and grow your team</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Training & Development module - Enhanced with IBM Watsonx")

def show_compensation():
    show_ibm_header()
    st.markdown("""
    <div class="ibm-page-header">
        <h1 class="ibm-type-alpha">Compensation</h1>
        <p class="ibm-type-epsilon" style="color: #525252;">Salary benchmarking and benefits</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Compensation module - Enhanced with IBM Watsonx")

def show_analytics():
    show_ibm_header()
    st.markdown("""
    <div class="ibm-page-header">
        <h1 class="ibm-type-alpha">Analytics</h1>
        <p class="ibm-type-epsilon" style="color: #525252;">Data-driven workforce insights</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Analytics module - Enhanced with IBM Watsonx")

# Authentication Page with IBM Design
def show_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="max-width: 400px; margin: 4rem auto; padding: 2rem;">
            <div style="text-align: center; margin-bottom: 3rem;">
                <h1 class="ibm-type-alpha" style="color: #161616; margin-bottom: 0.5rem;">TalentPilot</h1>
                <p class="ibm-type-epsilon" style="color: #525252;">AI HR Orchestration Platform</p>
                <div style="background: #0f62fe; color: white; padding: 0.5rem 1rem; display: inline-block; margin-top: 1rem;">
                    <span class="ibm-type-zeta">Powered by IBM Watsonx</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            placeholder="Enter your API key...",
            help="Get your API key from https://openrouter.ai/keys"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Connect", use_container_width=True):
                if api_key:
                    st.session_state.api_key = api_key
                    st.session_state.authenticated = True
                    st.session_state.demo_mode = False
                    st.success("Connected successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Please enter your API key")
        
        with col_btn2:
            if st.button("Demo Mode", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.demo_mode = True
                st.success("Entering Demo Mode...")
                time.sleep(1)
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Main Application
def main():
    init_session_state()
    
    if not st.session_state.authenticated:
        show_auth_page()
        return
    
    show_ibm_sidebar()
    
    page_mapping = {
        "Dashboard": show_dashboard,
        "Recruitment": show_recruitment,
        "Employee Directory": show_employee_directory,
        "Performance Reviews": show_performance,
        "Offer Letters": show_offer_letters,
        "Training & Development": show_training,
        "Compensation": show_compensation,
        "Analytics": show_analytics,
        "AI Assistant": show_ai_assistant
    }
    
    current_function = page_mapping.get(st.session_state.current_page, show_dashboard)
    current_function()

if __name__ == "__main__":
    main()
