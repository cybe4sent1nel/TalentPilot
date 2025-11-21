import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="TalentPilot - HR Management",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# HEPro-Inspired Design System
# Color Palette: Professional, Clean, Modern
COLORS = {
    # Primary Colors (HEPro-inspired)
    "primary": "#2563eb",          # Deep Blue
    "primary_light": "#3b82f6",    # Light Blue
    "primary_dark": "#1e40af",     # Dark Blue
    
    # Accent Colors
    "accent": "#10b981",           # Green (Success)
    "accent_orange": "#f97316",    # Orange (Warning)
    "accent_red": "#ef4444",       # Red (Danger)
    "accent_purple": "#8b5cf6",    # Purple (Info)
    
    # Neutral Colors
    "dark": "#1f2937",             # Almost Black
    "light": "#f9fafb",            # Almost White
    "gray": "#6b7280",             # Medium Gray
    "gray_light": "#e5e7eb",       # Light Gray
    "white": "#ffffff",            # Pure White
    
    # Status Colors
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#3b82f6"
}

# HEPro-Style CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
    }}
    
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {COLORS['light']};
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(135deg, {COLORS['white']} 0%, #f3f4f6 100%);
        border-right: 1px solid {COLORS['gray_light']};
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: {COLORS['dark']};
    }}
    
    /* Logo & Header */
    .logo-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem 1rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid {COLORS['gray_light']};
    }}
    
    .logo-box {{
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent_purple']} 100%);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: {COLORS['white']};
        font-weight: 800;
        font-size: 24px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }}
    
    .logo-text {{
        margin-left: 0.75rem;
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['dark']};
        letter-spacing: -0.5px;
    }}
    
    /* Cards & Containers */
    .metric-card {{
        background: {COLORS['white']};
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid {COLORS['gray_light']};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border-color: {COLORS['primary_light']};
    }}
    
    .feature-card {{
        background: {COLORS['white']};
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid {COLORS['gray_light']};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }}
    
    .feature-card:hover {{
        border-color: {COLORS['primary_light']};
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.12);
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%);
        color: {COLORS['white']};
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        letter-spacing: 0.3px;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
    }}
    
    /* Authentication Container */
    .auth-container {{
        max-width: 420px;
        margin: 4rem auto;
        background: {COLORS['white']};
        border-radius: 18px;
        padding: 3rem 2.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid {COLORS['gray_light']};
    }}
    
    .auth-title {{
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        color: {COLORS['dark']};
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }}
    
    .auth-subtitle {{
        text-align: center;
        color: {COLORS['gray']};
        font-size: 14px;
        margin-bottom: 2rem;
        font-weight: 500;
    }}
    
    /* Headers */
    .page-title {{
        font-size: 32px;
        font-weight: 800;
        color: {COLORS['dark']};
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }}
    
    .page-subtitle {{
        font-size: 15px;
        color: {COLORS['gray']};
        font-weight: 500;
        margin-bottom: 2rem;
    }}
    
    /* Metric Values */
    .metric-value {{
        font-size: 36px;
        font-weight: 800;
        color: {COLORS['primary']};
        margin: 0.75rem 0;
        letter-spacing: -1px;
    }}
    
    .metric-label {{
        font-size: 13px;
        color: {COLORS['gray']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .metric-change {{
        font-size: 12px;
        color: {COLORS['accent']};
        font-weight: 700;
        margin-top: 0.5rem;
    }}
    
    /* Badges */
    .badge {{
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .badge-success {{
        background: rgba({16}, {185}, {129}, 0.12);
        color: {COLORS['accent']};
    }}
    
    .badge-warning {{
        background: rgba({249}, {115}, {22}, 0.12);
        color: {COLORS['accent_orange']};
    }}
    
    .badge-danger {{
        background: rgba({239}, {68}, {68}, 0.12);
        color: {COLORS['accent_red']};
    }}
    
    .badge-info {{
        background: rgba({37}, {99}, {235}, 0.12);
        color: {COLORS['primary']};
    }}
    
    /* Activity Items */
    .activity-item {{
        padding: 1.25rem;
        border-left: 3px solid {COLORS['gray_light']};
        margin-bottom: 1rem;
        background: {COLORS['white']};
        border-radius: 10px;
        transition: all 0.3s ease;
    }}
    
    .activity-item:hover {{
        border-left-color: {COLORS['primary']};
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
    }}
    
    /* Kanban Cards */
    .kanban-column {{
        background: {COLORS['light']};
        border-radius: 12px;
        padding: 1.25rem;
        min-height: 500px;
    }}
    
    .kanban-card {{
        background: {COLORS['white']};
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid {COLORS['primary']};
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        cursor: move;
        transition: all 0.3s ease;
    }}
    
    .kanban-card:hover {{
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }}
    
    /* Response Container */
    .response-container {{
        background: linear-gradient(135deg, rgba({37}, {99}, {235}, 0.08) 0%, rgba({139}, {92}, {246}, 0.08) 100%);
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid {COLORS['gray_light']};
        margin-top: 1.5rem;
    }}
    
    .response-header {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        color: {COLORS['primary_dark']};
        font-weight: 700;
        font-size: 16px;
    }}
    
    .response-content {{
        background: {COLORS['white']};
        border-radius: 10px;
        padding: 1.25rem;
        color: {COLORS['dark']};
        line-height: 1.7;
        font-size: 14px;
    }}
    
    /* Input Fields */
    .stTextInput > div > div > input {{
        border-radius: 10px;
        border: 1px solid {COLORS['gray_light']};
        padding: 0.75rem 1rem;
        font-size: 14px;
    }}
    
    .stSelectbox > div > div > select {{
        border-radius: 10px;
        border: 1px solid {COLORS['gray_light']};
        padding: 0.75rem 1rem;
        font-size: 14px;
    }}
    
    .stTextArea > div > div > textarea {{
        border-radius: 10px;
        border: 1px solid {COLORS['gray_light']};
        padding: 0.75rem 1rem;
        font-size: 14px;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        color: {COLORS['gray']};
    }}
    
    /* User Info Box */
    .user-info-box {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent_purple']} 100%);
        border-radius: 12px;
        padding: 1.25rem;
        color: {COLORS['white']};
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }}
    
    .user-name {{
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 0.25rem;
    }}
    
    .user-company {{
        font-size: 12px;
        opacity: 0.9;
        font-weight: 500;
    }}
    
    /* Section Headers */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid {COLORS['primary_light']};
    }}
    
    .section-title {{
        font-size: 18px;
        font-weight: 700;
        color: {COLORS['dark']};
    }}
    
    /* Chat Interface */
    .chat-message-user {{
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1rem;
    }}
    
    .chat-message-user-content {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%);
        color: {COLORS['white']};
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        max-width: 70%;
        font-size: 14px;
        border-bottom-right-radius: 4px;
    }}
    
    .chat-message-bot {{
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1rem;
    }}
    
    .chat-message-bot-content {{
        background: {COLORS['light']};
        color: {COLORS['dark']};
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        max-width: 80%;
        font-size: 14px;
        border: 1px solid {COLORS['gray_light']};
        border-bottom-left-radius: 4px;
    }}
    
    /* Demo Badge */
    .demo-badge {{
        display: inline-block;
        background: {COLORS['accent_orange']};
        color: {COLORS['white']};
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        margin-left: 0.75rem;
        box-shadow: 0 2px 8px rgba({249}, {115}, {22}, 0.3);
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .metric-value {{ font-size: 24px; }}
        .page-title {{ font-size: 24px; }}
    }}
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
        'user_name': 'Alex Johnson',
        'company_name': 'TechCorp Inc.',
        'employee_count': 1234,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Sample Data Generation
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
            'skills': ['SEO', 'Content Strategy', 'Analytics'],
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
            'skills': ['Sales Strategy', 'CRM', 'Leadership'],
            'performance_score': 4.8,
            'pto_balance': 8
        },
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
        },
    ]

def generate_sample_candidates():
    return [
        {
            'id': 'CAN001',
            'name': 'Alex Thompson',
            'email': 'alex.t@email.com',
            'position_applied': 'Senior Full-Stack Developer',
            'status': 'Phone Screen',
            'score': 85,
            'experience': '7 years',
        },
        {
            'id': 'CAN002',
            'name': 'Jordan Lee',
            'email': 'jordan.l@email.com',
            'position_applied': 'Product Manager',
            'status': 'Technical Interview',
            'score': 92,
            'experience': '5 years',
        }
    ]

def generate_notifications():
    return [
        {'id': 1, 'type': 'urgent', 'message': '3 interviews scheduled for today', 'time': '2 hours ago'},
        {'id': 2, 'type': 'info', 'message': 'New performance review templates available', 'time': '5 hours ago'},
        {'id': 3, 'type': 'success', 'message': '5 new job applications received', 'time': '1 day ago'},
    ]

def generate_tasks():
    return [
        {'id': 1, 'title': 'Review Sarah Johnson\'s performance', 'priority': 'High', 'due': '2024-02-10', 'status': 'In Progress'},
        {'id': 2, 'title': 'Schedule interviews for PM role', 'priority': 'High', 'due': '2024-02-08', 'status': 'To Do'},
        {'id': 3, 'title': 'Update employee handbook', 'priority': 'Medium', 'due': '2024-02-15', 'status': 'To Do'},
    ]

# API Call Function
def call_openrouter_api(prompt):
    """Call OpenRouter API"""
    if st.session_state.demo_mode:
        time.sleep(1)
        return "Demo response: " + prompt[:50] + "..."
    
    try:
        headers = {
            'Authorization': f'Bearer {st.session_state.api_key}',
            'Content-Type': 'application/json',
        }
        
        data = {
            'model': 'openai/gpt-3.5-turbo',
            'messages': [
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
                <div class="logo-box" style="margin: 0 auto; width: 72px; height: 72px; font-size: 36px;">TP</div>
            </div>
            <h1 class="auth-title">TalentPilot</h1>
            <p class="auth-subtitle">AI-Powered HR Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            placeholder="sk-or-v1-...",
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("Connect", use_container_width=True, type="primary"):
                if api_key:
                    st.session_state.api_key = api_key
                    st.session_state.authenticated = True
                    st.session_state.demo_mode = False
                    st.success("Connected")
                    time.sleep(1)
                    st.rerun()
        
        with col_btn2:
            if st.button("Demo Mode", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.demo_mode = True
                st.success("Demo mode")
                time.sleep(1)
                st.rerun()

# Sidebar Navigation
def show_sidebar():
    """Display sidebar"""
    with st.sidebar:
        st.markdown("""
        <div class="logo-container">
            <div class="logo-box">TP</div>
            <div class="logo-text">TalentPilot</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="user-info-box">
            <div class="user-name">{st.session_state.user_name}</div>
            <div class="user-company">{st.session_state.company_name}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.demo_mode:
            st.info("Demo Mode - Sample data only", icon="ℹ️")
        
        st.markdown("### NAVIGATION")
        
        pages = {
            "Dashboard": "Dashboard",
            "Employees": "Employee Directory",
            "Recruitment": "Recruitment",
            "Tasks": "Tasks",
            "AI Chat": "AI Assistant"
        }
        
        for label, page in pages.items():
            is_active = st.session_state.current_page == page
            if st.button(
                label, 
                use_container_width=True, 
                key=page,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("### OVERVIEW")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Employees", st.session_state.employee_count)
        with col2:
            st.metric("Open Jobs", len(st.session_state.job_postings))
        
        st.metric("Pending Tasks", len([t for t in st.session_state.tasks if t['status'] != 'Done']))
        
        st.markdown("---")
        
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# Dashboard Page
def show_dashboard():
    """Display dashboard"""
    st.markdown("""
    <div style="margin-bottom: 2.5rem;">
        <h1 class="page-title">Welcome back, Alex</h1>
        <p class="page-subtitle">Here's your HR dashboard for today</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("Total Employees", "1,234", "+12%"),
        ("Open Positions", "23", "+5"),
        ("Pending Reviews", "45", "15 due"),
        ("Training Progress", "78%", "+8%"),
        ("Satisfaction", "8.4/10", "+0.3")
    ]
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Employees</div>
            <div class="metric-value">1,234</div>
            <div class="metric-change">↗ +12% from last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Open Positions</div>
            <div class="metric-value">23</div>
            <div class="metric-change">↗ +5 this week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Pending Reviews</div>
            <div class="metric-value">45</div>
            <div class="metric-change">📌 15 due this week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Training Progress</div>
            <div class="metric-value">78%</div>
            <div class="metric-change">↗ +8% completion</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Satisfaction</div>
            <div class="metric-value">8.4</div>
            <div class="metric-change">↗ +0.3 points</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Activity & Quick Actions
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("""<div class="section-header">
            <div class="section-title">Recent Activity</div>
        </div>""", unsafe_allow_html=True)
        
        activities = [
            ("New hire onboarded", "Sarah Johnson - Software Engineer", "2 hours ago"),
            ("Interview scheduled", "Michael Chen - Product Manager", "5 hours ago"),
            ("Performance review completed", "Emily Davis - Sales Director", "1 day ago"),
        ]
        
        for title, desc, time_ago in activities:
            st.markdown(f"""
            <div class="activity-item">
                <div style="font-weight: 700; color: {COLORS['dark']}; margin-bottom: 0.25rem;">{title}</div>
                <div style="font-size: 13px; color: {COLORS['gray']}; margin-bottom: 0.25rem;">{desc}</div>
                <div style="font-size: 12px; color: #9ca3af;">{time_ago}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""<div class="section-header">
            <div class="section-title">Quick Actions</div>
        </div>""", unsafe_allow_html=True)
        
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
    <div style="margin-bottom: 2rem;">
        <h1 class="page-title">Employee Directory</h1>
        <p class="page-subtitle">Manage all employee information</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search = st.text_input("Search employees", placeholder="Name, role, department...")
    with col2:
        dept = st.selectbox("Department", ["All"] + list(set([e['department'] for e in st.session_state.employees])))
    with col3:
        status = st.selectbox("Status", ["All", "Active", "On Leave"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    for emp in st.session_state.employees:
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; gap: 1.5rem; justify-content: space-between;">
                <div style="flex: 1;">
                    <div style="font-weight: 700; color: {COLORS['dark']}; font-size: 18px; margin-bottom: 0.25rem;">
                        {emp['name']}
                    </div>
                    <div style="color: {COLORS['primary']}; font-weight: 600; margin-bottom: 0.75rem;">
                        {emp['role']}
                    </div>
                    <div style="display: flex; gap: 1rem; font-size: 13px; color: {COLORS['gray']};">
                        <span>{emp['department']}</span>
                        <span>|</span>
                        <span>{emp['email']}</span>
                        <span>|</span>
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
    """Display recruitment"""
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 class="page-title">Recruitment Hub</h1>
        <p class="page-subtitle">Manage job postings and candidates</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Open Positions</div>
            <div class="metric-value">23</div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Applications</div>
            <div class="metric-value">145</div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">In Interview</div>
            <div class="metric-value">18</div>
        </div>""", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Avg Time to Hire</div>
            <div class="metric-value">28d</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Job Postings", "Candidates", "AI Tools"])
    
    with tab1:
        st.markdown("""<div class="section-header">
            <div class="section-title">Active Job Postings</div>
        </div>""", unsafe_allow_html=True)
        
        for job in st.session_state.job_postings:
            st.markdown(f"""
            <div class="feature-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div style="font-weight: 700; color: {COLORS['dark']}; font-size: 18px;">{job['title']}</div>
                        <div style="display: flex; gap: 1rem; font-size: 13px; color: {COLORS['gray']}; margin-top: 0.5rem;">
                            <span>{job['location']}</span>
                            <span>|</span>
                            <span>{job['type']}</span>
                            <span>|</span>
                            <span>{job['salary_range']}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 700; color: {COLORS['primary']}; font-size: 24px;">
                            {job['applications']}
                        </div>
                        <div style="font-size: 12px; color: {COLORS['gray']};">applications</div>
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
        st.markdown("""<div class="section-header">
            <div class="section-title">Candidates Pipeline</div>
        </div>""", unsafe_allow_html=True)
        
        for candidate in st.session_state.candidates:
            st.markdown(f"""
            <div class="feature-card">
                <div style="display: flex; gap: 1.5rem; justify-content: space-between;">
                    <div style="flex: 1;">
                        <div style="font-weight: 700; color: {COLORS['dark']}; font-size: 18px;">{candidate['name']}</div>
                        <div style="color: {COLORS['gray']}; margin-top: 0.25rem;">{candidate['position_applied']}</div>
                        <div style="display: flex; gap: 1rem; font-size: 12px; color: {COLORS['gray']}; margin-top: 0.5rem;">
                            <span>{candidate['email']}</span>
                            <span>|</span>
                            <span>{candidate['experience']}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 700; color: {COLORS['accent']}; font-size: 24px;">
                            {candidate['score']}
                        </div>
                        <div style="font-size: 12px; color: {COLORS['gray']};">AI Score</div>
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
        st.markdown("""<div class="section-header">
            <div class="section-title">AI-Powered Tools</div>
        </div>""", unsafe_allow_html=True)
        
        job_input = st.text_area("Describe the job", placeholder="Senior Software Engineer with 5+ years in React...")
        
        if st.button("Generate Description", use_container_width=True, type="primary"):
            if job_input:
                with st.spinner("Generating..."):
                    response = call_openrouter_api(f"Generate job description for: {job_input}")
                    st.markdown(f"""<div class="response-container">
                    <div class="response-header">Generated Description</div>
                    <div class="response-content">{response}</div>
                    </div>""", unsafe_allow_html=True)

# Tasks Page
def show_tasks():
    """Display tasks"""
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 class="page-title">Task Management</h1>
        <p class="page-subtitle">Track and manage your tasks</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(st.session_state.tasks)
    completed = len([t for t in st.session_state.tasks if t['status'] == 'Done'])
    
    with col1:
        st.metric("Total Tasks", total)
    with col2:
        st.metric("Completed", completed)
    with col3:
        st.metric("High Priority", len([t for t in st.session_state.tasks if t['priority'] == 'High']))
    with col4:
        st.metric("Completion", f"{int(completed/max(total, 1)*100)}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    statuses = ["To Do", "In Progress", "Planning", "Done"]
    
    for col, status in zip([col1, col2, col3, col4], statuses):
        with col:
            st.markdown(f"### {status}")
            tasks = [t for t in st.session_state.tasks if t['status'] == status]
            
            for task in tasks:
                priority_color = {"High": COLORS['accent_red'], "Medium": COLORS['accent_orange'], "Low": COLORS['primary']}[task['priority']]
                
                st.markdown(f"""
                <div class="kanban-card" style="border-left-color: {priority_color};">
                    <div style="font-weight: 600; color: {COLORS['dark']};">{task['title']}</div>
                    <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
                        <span class="badge" style="background: {priority_color}20; color: {priority_color};">
                            {task['priority']}
                        </span>
                    </div>
                    <div style="font-size: 12px; color: {COLORS['gray']}; margin-top: 0.5rem;">
                        Due: {task['due']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# AI Assistant
def show_ai_assistant():
    """Display AI assistant"""
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 class="page-title">AI Assistant</h1>
        <p class="page-subtitle">Your intelligent HR co-pilot</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div class="section-header">
        <div class="section-title">Quick Prompts</div>
    </div>""", unsafe_allow_html=True)
    
    prompts = [
        "Generate a job description for a Data Scientist",
        "Create an onboarding plan for a Marketing Manager",
        "Write performance review questions",
    ]
    
    cols = st.columns(3)
    for idx, prompt in enumerate(prompts):
        col = cols[idx % 3]
        with col:
            if st.button(prompt, use_container_width=True, key=f"prompt_{idx}"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                response = call_openrouter_api(prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        st.markdown("""<div class="section-header">
            <div class="section-title">Conversation</div>
        </div>""", unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message-user">
                    <div class="chat-message-user-content">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message-bot">
                    <div class="chat-message-bot-content">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {COLORS['gray']}; font-size: 13px; padding: 1.5rem;">
        <p style="font-weight: 700; margin: 0;">TalentPilot</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 12px;">AI-Powered HR Management System</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
