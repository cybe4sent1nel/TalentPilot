import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time
import random
import base64
from io import BytesIO
import calendar

# Page configuration
st.set_page_config(page_title="TalentPilot - AI HR Platform", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# IBM-Inspired CSS with Light Green/White Gradient
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
* { font-family: 'IBM Plex Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.main { background: linear-gradient(135deg, #f0fff4 0%, #ffffff 25%, #f0fdf4 50%, #ecfdf5 75%, #f0fff4 100%); background-attachment: fixed; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #064e3b 0%, #065f46 30%, #047857 60%, #059669 100%); border-right: 3px solid #10b981; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: #ecfdf5; }
.ibm-logo-container { display: flex; align-items: center; justify-content: center; padding: 2rem 1rem; margin-bottom: 1.5rem; border-bottom: 2px solid rgba(167, 243, 208, 0.3); background: linear-gradient(135deg, rgba(5, 150, 105, 0.2), rgba(16, 185, 129, 0.1)); border-radius: 0 0 20px 20px; }
.ibm-logo-box { width: 70px; height: 70px; background: linear-gradient(135deg, #10b981, #34d399, #6ee7b7); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 32px; box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4); transition: all 0.3s ease; }
.ibm-logo-box:hover { transform: scale(1.05) rotate(3deg); }
.ibm-logo-text { margin-left: 1rem; font-size: 24px; font-weight: 700; color: #ecfdf5; letter-spacing: -0.5px; }
.ibm-stat-card { background: linear-gradient(145deg, #ffffff, #f0fdf4); border-radius: 12px; padding: 1.75rem; box-shadow: 0 4px 24px rgba(5, 150, 105, 0.08); border: 1px solid rgba(16, 185, 129, 0.12); transition: all 0.3s ease; position: relative; overflow: hidden; height: 100%; }
.ibm-stat-card::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #10b981, #34d399); }
.ibm-stat-card:hover { transform: translateY(-6px) scale(1.02); box-shadow: 0 16px 48px rgba(5, 150, 105, 0.18); }
.ibm-stat-icon { width: 56px; height: 56px; background: linear-gradient(135deg, #d1fae5, #a7f3d0); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 28px; margin-bottom: 1rem; }
.ibm-stat-value { font-size: 36px; font-weight: 700; color: #064e3b; font-family: 'IBM Plex Mono', monospace; margin-bottom: 0.5rem; }
.ibm-stat-label { font-size: 14px; font-weight: 500; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }
.ibm-stat-trend { display: inline-flex; align-items: center; gap: 4px; font-size: 13px; font-weight: 600; padding: 4px 10px; border-radius: 20px; margin-top: 0.75rem; }
.ibm-stat-trend.positive { background: linear-gradient(135deg, #d1fae5, #a7f3d0); color: #047857; }
.ibm-feature-card { background: linear-gradient(145deg, #ffffff, #f0fdf4); border-radius: 16px; padding: 2rem; box-shadow: 0 4px 24px rgba(5, 150, 105, 0.08); border: 2px solid rgba(16, 185, 129, 0.1); transition: all 0.4s ease; height: 100%; }
.ibm-feature-card:hover { border-color: #10b981; box-shadow: 0 20px 60px rgba(5, 150, 105, 0.18); transform: translateY(-8px); }
.ibm-auth-container { max-width: 520px; margin: 3rem auto; background: linear-gradient(145deg, #ffffff, #f0fdf4, #ecfdf5); border-radius: 24px; padding: 3rem; box-shadow: 0 25px 80px rgba(5, 150, 105, 0.15); border: 2px solid rgba(16, 185, 129, 0.15); position: relative; overflow: hidden; }
.ibm-auth-container::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #059669, #10b981, #34d399, #6ee7b7); }
.ibm-auth-title { font-size: 42px; font-weight: 700; text-align: center; background: linear-gradient(135deg, #064e3b, #047857, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
.ibm-auth-subtitle { text-align: center; color: #6b7280; font-size: 16px; margin-bottom: 2.5rem; }
.stButton > button { width: 100%; background: linear-gradient(135deg, #059669, #10b981, #34d399); color: white; border: none; border-radius: 12px; padding: 0.875rem 1.75rem; font-weight: 600; font-size: 15px; transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35); }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(16, 185, 129, 0.45); }
.ibm-response-container { background: linear-gradient(145deg, #ecfdf5, #d1fae5, #a7f3d0); border-radius: 16px; padding: 2rem; border: 2px solid #10b981; margin-top: 2rem; position: relative; }
.ibm-response-container::before { content: ''; position: absolute; top: 0; left: 0; width: 6px; height: 100%; background: linear-gradient(180deg, #059669, #10b981, #34d399); }
.ibm-response-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; color: #064e3b; font-weight: 700; font-size: 18px; padding-left: 1rem; }
.ibm-response-content { background: white; border-radius: 12px; padding: 1.75rem; color: #1f2937; line-height: 1.8; white-space: pre-wrap; font-size: 14px; margin-left: 1rem; }
.ibm-demo-badge { display: inline-flex; align-items: center; gap: 6px; background: linear-gradient(135deg, #10b981, #34d399); color: white; padding: 6px 14px; border-radius: 24px; font-size: 12px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); animation: pulse-badge 2s infinite; }
@keyframes pulse-badge { 0%, 100% { box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); } 50% { box-shadow: 0 4px 24px rgba(16, 185, 129, 0.5); } }
.ibm-activity-item { padding: 1.25rem; border-left: 4px solid #d1fae5; margin-bottom: 1rem; background: linear-gradient(90deg, rgba(240, 253, 244, 0.5), transparent); transition: all 0.3s ease; border-radius: 0 12px 12px 0; }
.ibm-activity-item:hover { border-left-color: #10b981; background: linear-gradient(90deg, rgba(209, 250, 229, 0.6), rgba(240, 253, 244, 0.3)); transform: translateX(8px); }
.ibm-kanban-column { background: linear-gradient(180deg, #f0fdf4, #ecfdf5); border-radius: 16px; padding: 1.25rem; min-height: 450px; border: 1px solid rgba(16, 185, 129, 0.15); }
.ibm-kanban-card { background: white; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; border-left: 5px solid #10b981; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06); transition: all 0.3s ease; }
.ibm-kanban-card:hover { box-shadow: 0 8px 24px rgba(5, 150, 105, 0.15); transform: translateY(-4px); }
.ibm-employee-card { background: linear-gradient(145deg, #ffffff, #f0fdf4); border-radius: 20px; padding: 2rem; box-shadow: 0 8px 32px rgba(5, 150, 105, 0.1); border: 1px solid rgba(16, 185, 129, 0.12); transition: all 0.4s ease; position: relative; overflow: hidden; }
.ibm-employee-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px; background: linear-gradient(90deg, #059669, #10b981, #34d399, #6ee7b7); }
.ibm-employee-card:hover { transform: translateY(-8px); box-shadow: 0 20px 60px rgba(5, 150, 105, 0.18); }
.ibm-avatar { width: 80px; height: 80px; background: linear-gradient(135deg, #10b981, #34d399, #6ee7b7); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 36px; color: white; font-weight: 700; box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3); border: 4px solid white; }
.ibm-skill-tag { display: inline-block; padding: 4px 12px; background: linear-gradient(135deg, #ecfdf5, #d1fae5); color: #064e3b; border-radius: 8px; font-size: 12px; font-weight: 500; margin: 3px; border: 1px solid rgba(16, 185, 129, 0.2); }
.ibm-progress-container { background: #e5e7eb; border-radius: 10px; height: 12px; overflow: hidden; }
.ibm-progress-bar { height: 100%; background: linear-gradient(90deg, #059669, #10b981, #34d399); border-radius: 10px; transition: width 0.6s ease; }
.ibm-chat-bubble-user { background: linear-gradient(135deg, #059669, #10b981); color: white; padding: 1rem 1.25rem; border-radius: 18px 18px 6px 18px; max-width: 75%; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25); }
.ibm-chat-bubble-assistant { background: linear-gradient(145deg, #f0fdf4, #ecfdf5); color: #1f2937; padding: 1rem 1.25rem; border-radius: 18px 18px 18px 6px; max-width: 80%; border: 1px solid rgba(16, 185, 129, 0.15); }
.ibm-footer { text-align: center; padding: 2rem; color: #6b7280; font-size: 13px; border-top: 2px solid rgba(16, 185, 129, 0.15); background: linear-gradient(180deg, transparent, rgba(240, 253, 244, 0.5)); margin-top: 3rem; }
.ibm-footer-brand { font-weight: 700; background: linear-gradient(135deg, #059669, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
hr { border: none; height: 2px; background: linear-gradient(90deg, transparent, #d1fae5, #10b981, #d1fae5, transparent); margin: 2rem 0; }
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: #f0fdf4; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #10b981, #34d399); border-radius: 5px; }
[data-testid="stMetricValue"] { font-family: 'IBM Plex Mono', monospace; color: #064e3b; font-weight: 700; }
.stTabs [data-baseweb="tab"] { background: linear-gradient(145deg, #f0fdf4, #ecfdf5); border-radius: 10px 10px 0 0; padding: 0.75rem 1.5rem; font-weight: 600; }
.stTabs [aria-selected="true"] { background: linear-gradient(145deg, #10b981, #34d399) !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# Data Generators
def generate_sample_employees():
    return [
        {'id': 'EMP001', 'name': 'Sarah Johnson', 'role': 'Senior Software Engineer', 'department': 'Engineering', 'email': 'sarah.j@company.com', 'phone': '+1 (555) 123-4567', 'hire_date': '2021-03-15', 'salary': 125000, 'status': 'Active', 'manager': 'John Smith', 'location': 'San Francisco, CA', 'skills': ['Python', 'React', 'AWS', 'Docker'], 'performance_score': 4.5, 'pto_balance': 15, 'team': 'Platform'},
        {'id': 'EMP002', 'name': 'Michael Chen', 'role': 'Marketing Manager', 'department': 'Marketing', 'email': 'michael.c@company.com', 'phone': '+1 (555) 234-5678', 'hire_date': '2020-07-20', 'salary': 95000, 'status': 'Active', 'manager': 'Lisa Wong', 'location': 'New York, NY', 'skills': ['SEO', 'Content Strategy', 'Analytics'], 'performance_score': 4.2, 'pto_balance': 12, 'team': 'Growth'},
        {'id': 'EMP003', 'name': 'Emily Davis', 'role': 'Sales Director', 'department': 'Sales', 'email': 'emily.d@company.com', 'phone': '+1 (555) 345-6789', 'hire_date': '2019-01-10', 'salary': 135000, 'status': 'Active', 'manager': 'Robert Brown', 'location': 'Chicago, IL', 'skills': ['Sales Strategy', 'CRM', 'Negotiation'], 'performance_score': 4.8, 'pto_balance': 8, 'team': 'Enterprise'},
        {'id': 'EMP004', 'name': 'James Wilson', 'role': 'HR Specialist', 'department': 'HR', 'email': 'james.w@company.com', 'phone': '+1 (555) 456-7890', 'hire_date': '2022-05-01', 'salary': 75000, 'status': 'On Leave', 'manager': 'Patricia Lee', 'location': 'Austin, TX', 'skills': ['Recruitment', 'HRIS', 'Compliance'], 'performance_score': 4.0, 'pto_balance': 3, 'team': 'People Ops'},
        {'id': 'EMP005', 'name': 'Amanda Foster', 'role': 'Product Manager', 'department': 'Product', 'email': 'amanda.f@company.com', 'phone': '+1 (555) 567-8901', 'hire_date': '2021-09-01', 'salary': 115000, 'status': 'Active', 'manager': 'David Kim', 'location': 'Seattle, WA', 'skills': ['Agile', 'User Research', 'Roadmapping'], 'performance_score': 4.6, 'pto_balance': 10, 'team': 'Core Product'},
        {'id': 'EMP006', 'name': 'Robert Martinez', 'role': 'DevOps Engineer', 'department': 'Engineering', 'email': 'robert.m@company.com', 'phone': '+1 (555) 678-9012', 'hire_date': '2020-11-15', 'salary': 130000, 'status': 'Active', 'manager': 'John Smith', 'location': 'Remote', 'skills': ['Kubernetes', 'Terraform', 'CI/CD'], 'performance_score': 4.4, 'pto_balance': 14, 'team': 'Infrastructure'},
    ]

def generate_sample_jobs():
    return [
        {'id': 'JOB001', 'title': 'Senior Full-Stack Developer', 'department': 'Engineering', 'location': 'Remote', 'type': 'Full-time', 'salary_range': '$120k - $160k', 'posted_date': '2024-01-15', 'applications': 45, 'status': 'Open', 'description': 'Looking for an experienced full-stack developer...'},
        {'id': 'JOB002', 'title': 'Product Manager', 'department': 'Product', 'location': 'San Francisco, CA', 'type': 'Full-time', 'salary_range': '$130k - $170k', 'posted_date': '2024-01-20', 'applications': 32, 'status': 'Open', 'description': 'Seeking a strategic product manager...'},
        {'id': 'JOB003', 'title': 'DevOps Engineer', 'department': 'Engineering', 'location': 'Hybrid - NYC', 'type': 'Full-time', 'salary_range': '$110k - $150k', 'posted_date': '2024-01-25', 'applications': 28, 'status': 'Interviewing', 'description': 'We need a skilled DevOps engineer...'},
        {'id': 'JOB004', 'title': 'Marketing Specialist', 'department': 'Marketing', 'location': 'Remote', 'type': 'Full-time', 'salary_range': '$70k - $90k', 'posted_date': '2024-01-28', 'applications': 56, 'status': 'Open', 'description': 'Join our growing marketing team...'},
    ]

def generate_sample_candidates():
    return [
        {'id': 'CAN001', 'name': 'Alex Thompson', 'email': 'alex.t@email.com', 'phone': '+1 (555) 111-2222', 'position_applied': 'Senior Full-Stack Developer', 'status': 'Phone Screen', 'score': 85, 'experience': '7 years', 'education': 'BS Computer Science', 'skills': ['React', 'Node.js', 'PostgreSQL', 'AWS'], 'applied_date': '2024-01-16', 'interview_date': '2024-02-05'},
        {'id': 'CAN002', 'name': 'Jordan Lee', 'email': 'jordan.l@email.com', 'phone': '+1 (555) 222-3333', 'position_applied': 'Product Manager', 'status': 'Technical Interview', 'score': 92, 'experience': '5 years', 'education': 'MBA + BS Engineering', 'skills': ['Product Strategy', 'Agile', 'Data Analysis'], 'applied_date': '2024-01-21', 'interview_date': '2024-02-08'},
        {'id': 'CAN003', 'name': 'Casey Morgan', 'email': 'casey.m@email.com', 'phone': '+1 (555) 333-4444', 'position_applied': 'DevOps Engineer', 'status': 'Final Round', 'score': 88, 'experience': '6 years', 'education': 'BS Information Systems', 'skills': ['Kubernetes', 'AWS', 'Terraform', 'Python'], 'applied_date': '2024-01-26', 'interview_date': '2024-02-10'},
    ]

def generate_notifications():
    return [
        {'id': 1, 'type': 'urgent', 'message': '3 interviews scheduled for today', 'time': '2 hours ago', 'read': False},
        {'id': 2, 'type': 'info', 'message': 'New performance review templates available', 'time': '5 hours ago', 'read': False},
        {'id': 3, 'type': 'success', 'message': '5 new job applications received', 'time': '1 day ago', 'read': True},
        {'id': 4, 'type': 'warning', 'message': '2 employees on leave expiring soon', 'time': '2 days ago', 'read': True},
    ]

def generate_tasks():
    return [
        {'id': 1, 'title': "Review Sarah Johnson's performance", 'priority': 'High', 'due': '2024-02-10', 'status': 'In Progress', 'assigned_to': 'HR Manager'},
        {'id': 2, 'title': 'Schedule interviews for PM role', 'priority': 'High', 'due': '2024-02-08', 'status': 'To Do', 'assigned_to': 'Recruiter'},
        {'id': 3, 'title': 'Update employee handbook', 'priority': 'Medium', 'due': '2024-02-15', 'status': 'To Do', 'assigned_to': 'HR Manager'},
        {'id': 4, 'title': 'Process Q1 bonuses', 'priority': 'High', 'due': '2024-02-20', 'status': 'To Do', 'assigned_to': 'Finance'},
        {'id': 5, 'title': 'Organize team building event', 'priority': 'Low', 'due': '2024-03-01', 'status': 'Planning', 'assigned_to': 'HR Manager'},
    ]

def generate_payroll_data():
    return [
        {'month': 'January', 'total': 485000, 'taxes': 121250, 'benefits': 72750, 'net': 290000},
        {'month': 'February', 'total': 492000, 'taxes': 123000, 'benefits': 73800, 'net': 295200},
        {'month': 'March', 'total': 498000, 'taxes': 124500, 'benefits': 74700, 'net': 298800},
    ]

def generate_benefits_data():
    return {
        'health_enrollment': 92, 'dental_enrollment': 85, 'vision_enrollment': 78,
        '401k_participation': 88, 'avg_401k_contribution': 8.5, 'hsa_enrollment': 45
    }

def generate_compliance_data():
    return [
        {'item': 'I-9 Verification', 'status': 'Compliant', 'due': '2024-03-01', 'completion': 100},
        {'item': 'OSHA Training', 'status': 'In Progress', 'due': '2024-02-28', 'completion': 85},
        {'item': 'Sexual Harassment Training', 'status': 'Compliant', 'due': '2024-06-01', 'completion': 100},
        {'item': 'Data Privacy Training', 'status': 'Action Required', 'due': '2024-02-15', 'completion': 72},
    ]

def generate_surveys():
    return [
        {'id': 1, 'name': 'Employee Engagement Survey', 'status': 'Active', 'responses': 234, 'total': 300, 'avg_score': 4.2},
        {'id': 2, 'name': 'Manager Feedback Survey', 'status': 'Completed', 'responses': 45, 'total': 45, 'avg_score': 4.5},
        {'id': 3, 'name': 'Onboarding Experience Survey', 'status': 'Active', 'responses': 12, 'total': 15, 'avg_score': 4.7},
    ]

def generate_documents():
    return [
        {'id': 1, 'name': 'Employee Handbook 2024', 'type': 'Policy', 'updated': '2024-01-15', 'size': '2.4 MB'},
        {'id': 2, 'name': 'Benefits Guide', 'type': 'Guide', 'updated': '2024-01-01', 'size': '1.8 MB'},
        {'id': 3, 'name': 'Code of Conduct', 'type': 'Policy', 'updated': '2023-12-01', 'size': '0.5 MB'},
        {'id': 4, 'name': 'Remote Work Policy', 'type': 'Policy', 'updated': '2024-01-20', 'size': '0.3 MB'},
    ]

def generate_org_chart():
    return {
        'CEO': {'name': 'John Anderson', 'reports': ['CTO', 'CFO', 'COO', 'CHRO']},
        'CTO': {'name': 'Sarah Mitchell', 'reports': ['VP Engineering', 'VP Product']},
        'CFO': {'name': 'Robert Chen', 'reports': ['VP Finance', 'Controller']},
        'COO': {'name': 'Emily Watson', 'reports': ['VP Operations', 'VP Sales']},
        'CHRO': {'name': 'Michael Brown', 'reports': ['VP HR', 'VP Talent']},
    }

def generate_time_tracking():
    return [
        {'employee': 'Sarah Johnson', 'hours_this_week': 42, 'overtime': 2, 'pto_used': 0},
        {'employee': 'Michael Chen', 'hours_this_week': 40, 'overtime': 0, 'pto_used': 0},
        {'employee': 'Emily Davis', 'hours_this_week': 45, 'overtime': 5, 'pto_used': 0},
    ]

def generate_goals():
    return [
        {'id': 1, 'title': 'Increase Employee Retention', 'progress': 75, 'due': 'Q2 2024', 'owner': 'HR Team'},
        {'id': 2, 'title': 'Reduce Time-to-Hire', 'progress': 60, 'due': 'Q1 2024', 'owner': 'Recruiting'},
        {'id': 3, 'title': 'Improve eNPS Score', 'progress': 45, 'due': 'Q3 2024', 'owner': 'People Ops'},
    ]

def generate_announcements():
    return [
        {'id': 1, 'title': '🎉 Q4 Results - Record Breaking!', 'date': '2024-01-28', 'priority': 'high'},
        {'id': 2, 'title': '📅 Company All-Hands: Feb 5th', 'date': '2024-01-25', 'priority': 'medium'},
        {'id': 3, 'title': '🏥 Open Enrollment Deadline Extended', 'date': '2024-01-22', 'priority': 'high'},
    ]

def generate_wellness_data():
    return {'mental_health_resources': 156, 'gym_reimbursements': 89, 'wellness_events': 12, 'avg_wellness_score': 7.8}

# Initialize Session State
def init_session_state():
    defaults = {
        'authenticated': False, 'api_key': '', 'demo_mode': False, 'current_page': 'Dashboard',
        'employees': generate_sample_employees(), 'job_postings': generate_sample_jobs(),
        'candidates': generate_sample_candidates(), 'notifications': generate_notifications(),
        'tasks': generate_tasks(), 'chat_history': [], 'user_name': 'HR Manager',
        'company_name': 'TechCorp Inc.', 'employee_count': 1234,
        'payroll_data': generate_payroll_data(), 'benefits_data': generate_benefits_data(),
        'compliance_data': generate_compliance_data(), 'surveys': generate_surveys(),
        'documents': generate_documents(), 'goals': generate_goals(),
        'announcements': generate_announcements(), 'wellness_data': generate_wellness_data(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# AI API Call
def call_openrouter_api(prompt, system_message="You are TalentPilot, an expert HR AI assistant."):
    if st.session_state.demo_mode:
        time.sleep(1.5)
        if 'job description' in prompt.lower():
            return """**Senior Software Engineer**\n\n**Summary:** We seek an experienced engineer to join our team.\n\n**Responsibilities:**\n• Design and develop scalable applications\n• Lead technical discussions and mentor juniors\n• Collaborate with cross-functional teams\n• Write clean, maintainable code\n\n**Requirements:**\n• 5+ years experience\n• Proficiency in Python, React, Node.js\n• Cloud platform experience (AWS/GCP)\n• Strong problem-solving skills\n\n**Benefits:**\n• Competitive salary: $120k-$160k\n• Health, dental, vision insurance\n• 401(k) matching\n• Unlimited PTO\n• Remote flexibility"""
        elif 'resume' in prompt.lower() or 'analyze' in prompt.lower():
            return """**📊 RESUME ANALYSIS REPORT**\n\n**Overall Score: 87/100** ⭐⭐⭐⭐⭐\n\n**Strengths:**\n• Strong technical expertise (9/10)\n• Excellent career progression\n• Quantifiable achievements\n• Leadership experience\n\n**Areas for Improvement:**\n• Add professional summary\n• Include more certifications\n• Optimize keywords\n\n**Recommendation: STRONG HIRE - PROCEED TO INTERVIEW**"""
        elif 'interview' in prompt.lower():
            return """**🎤 INTERVIEW QUESTIONS**\n\n**Technical:**\n1. Design a scalable URL shortening service\n2. Explain your approach to code optimization\n3. How do you handle technical debt?\n\n**Behavioral:**\n1. Tell me about a challenging project\n2. How do you handle disagreements?\n3. Describe your leadership style\n\n**Cultural Fit:**\n1. Why are you interested in this role?\n2. How do you stay current with technology?\n3. What's your ideal work environment?"""
        elif 'onboarding' in prompt.lower():
            return """**🚀 30-DAY ONBOARDING PLAN**\n\n**Week 1: Orientation**\n• Day 1: Welcome, IT setup, team lunch\n• Day 2-3: Systems training\n• Day 4-5: Team introductions\n\n**Week 2: Learning**\n• Deep dive into products\n• Shadow team members\n• Meet stakeholders\n\n**Week 3: Contributing**\n• Take ownership of projects\n• Lead first meeting\n• Start delivering\n\n**Week 4: Impact**\n• Full ownership\n• Present to leadership\n• 30-day review"""
        elif 'policy' in prompt.lower():
            return """**📋 HR POLICY TEMPLATE**\n\n**Purpose:** This policy establishes guidelines for...\n\n**Scope:** Applies to all employees...\n\n**Policy Statement:**\n1. General Guidelines\n2. Procedures\n3. Responsibilities\n4. Compliance\n\n**Effective Date:** Immediately\n**Review Date:** Annual"""
        else:
            return """**🤖 TalentPilot AI Assistant**\n\nI can help you with:\n\n• 📝 Generate job descriptions\n• 🎯 Analyze resumes\n• 💬 Create interview questions\n• 🚀 Design onboarding plans\n• 📋 Write HR policies\n• 📊 Performance reviews\n• 💰 Compensation analysis\n\nTry: "Generate a job description for [role]" """
    try:
        headers = {'Authorization': f'Bearer {st.session_state.api_key}', 'Content-Type': 'application/json'}
        data = {'model': 'openai/gpt-3.5-turbo', 'messages': [{'role': 'system', 'content': system_message}, {'role': 'user', 'content': prompt}], 'max_tokens': 2000}
        response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# Authentication Page
def show_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="ibm-auth-container">
            <div style="display: flex; justify-content: center; margin-bottom: 1.5rem;">
                <div class="ibm-logo-box">🚀</div>
            </div>
            <h1 class="ibm-auth-title">TalentPilot</h1>
            <p class="ibm-auth-subtitle">AI-Powered HR Orchestration Platform</p>
        </div>
        """, unsafe_allow_html=True)
        api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-v1-...")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Connect", use_container_width=True):
                if api_key:
                    st.session_state.api_key = api_key
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Please enter API key")
        with col_btn2:
            if st.button("🎮 Demo Mode", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.demo_mode = True
                st.rerun()
        st.markdown("---")
        cols = st.columns(4)
        features = [("🤖", "AI-Powered"), ("⚡", "Fast"), ("📊", "Analytics"), ("🔒", "Secure")]
        for col, (icon, title) in zip(cols, features):
            with col:
                st.markdown(f"<div style='text-align:center'><span style='font-size:32px'>{icon}</span><br><b>{title}</b></div>", unsafe_allow_html=True)

# Sidebar
def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="ibm-logo-container">
            <div class="ibm-logo-box">🚀</div>
            <div><div class="ibm-logo-text">TalentPilot</div><div style="color:#a7f3d0;font-size:11px">AI HR PLATFORM</div></div>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.demo_mode:
            st.markdown('<div class="ibm-demo-badge">🎮 DEMO MODE</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='background:rgba(255,255,255,0.1);border-radius:12px;padding:1rem;margin:1rem 0'><b style='color:white'>{st.session_state.user_name}</b><br><span style='color:#a7f3d0;font-size:13px'>{st.session_state.company_name}</span></div>", unsafe_allow_html=True)
        unread = sum(1 for n in st.session_state.notifications if not n['read'])
        if unread > 0:
            with st.expander(f"🔔 Notifications ({unread})"):
                for n in st.session_state.notifications[:3]:
                    if not n['read']:
                        st.markdown(f"**{n['message']}**\n{n['time']}")
        st.markdown("### 📋 Modules")
        pages = {"🏠 Dashboard": "Dashboard", "👥 Recruitment": "Recruitment", "📋 Onboarding": "Onboarding", "💼 Employees": "Employee Directory", "🎯 Performance": "Performance", "🎓 Training": "Training", "💰 Payroll": "Payroll", "🏥 Benefits": "Benefits", "📅 Time & Leave": "Time & Leave", "✅ Compliance": "Compliance", "📊 Analytics": "Analytics", "📝 Documents": "Documents", "📣 Announcements": "Announcements", "💬 AI Assistant": "AI Assistant"}
        for label, page in pages.items():
            if st.button(label, use_container_width=True, key=page, type="primary" if st.session_state.current_page == page else "secondary"):
                st.session_state.current_page = page
                st.rerun()
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.metric("Employees", st.session_state.employee_count)
        st.metric("Open Roles", len(st.session_state.job_postings))
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# Dashboard
def show_dashboard():
    hour = datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    st.markdown(f"<h1 style='color:#064e3b'>{greeting}, {st.session_state.user_name}! 👋 {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}</h1><p style='color:#6b7280'>Here's your HR overview for today</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(5)
    metrics = [("👥", "1,234", "Employees", "+12%", "positive"), ("💼", "23", "Open Roles", "+5", "positive"), ("🎯", "45", "Reviews Due", "15 this week", ""), ("🎓", "78%", "Training", "+8%", "positive"), ("😊", "8.4", "eNPS Score", "+0.3", "positive")]
    for col, (icon, value, label, trend, trend_class) in zip(cols, metrics):
        with col:
            st.markdown(f"""<div class="ibm-stat-card"><div class="ibm-stat-icon">{icon}</div><div class="ibm-stat-value">{value}</div><div class="ibm-stat-label">{label}</div><div class="ibm-stat-trend {trend_class}">↗ {trend}</div></div>""", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("### 📊 Recent Activity")
        activities = [("✅", "New hire onboarded", "Sarah Johnson - Software Engineer", "2h ago"), ("📅", "Interview scheduled", "Michael Chen - Product Manager", "5h ago"), ("⭐", "Performance review", "Emily Davis - Sales Director", "1 day ago"), ("⏳", "Leave request", "James Wilson - 3 days vacation", "2 days ago")]
        for icon, title, desc, time in activities:
            st.markdown(f"""<div class="ibm-activity-item"><div style="display:flex;align-items:center;gap:1rem"><span style="font-size:24px">{icon}</span><div style="flex:1"><b style="color:#1e293b">{title}</b><br><span style="color:#6b7280;font-size:14px">{desc}</span></div><span style="color:#94a3b8;font-size:12px">{time}</span></div></div>""", unsafe_allow_html=True)
        st.markdown("### 🎯 Company Goals")
        for goal in st.session_state.goals:
            st.markdown(f"**{goal['title']}** - {goal['owner']}")
            st.markdown(f"""<div class="ibm-progress-container"><div class="ibm-progress-bar" style="width:{goal['progress']}%"></div></div>""", unsafe_allow_html=True)
            st.caption(f"{goal['progress']}% complete • Due: {goal['due']}")
    with col_right:
        st.markdown("### ⚡ Quick Actions")
        if st.button("📝 Post New Job", use_container_width=True):
            st.session_state.current_page = "Recruitment"
            st.rerun()
        if st.button("👤 Add Employee", use_container_width=True):
            st.session_state.current_page = "Employee Directory"
            st.rerun()
        if st.button("💬 Ask AI Assistant", use_container_width=True):
            st.session_state.current_page = "AI Assistant"
            st.rerun()
        st.markdown("### 📣 Announcements")
        for ann in st.session_state.announcements:
            st.markdown(f"""<div class="ibm-kanban-card"><b>{ann['title']}</b><br><span style="color:#6b7280;font-size:12px">{ann['date']}</span></div>""", unsafe_allow_html=True)
        st.markdown("### ✅ Your Tasks")
        for task in [t for t in st.session_state.tasks if t['priority'] == 'High'][:3]:
            st.checkbox(task['title'], key=f"t_{task['id']}")
            st.caption(f"Due: {task['due']}")

# Employee Directory
def show_employee_directory():
    st.markdown(f"## 💼 Employee Directory {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("🔍 Search employees", placeholder="Name, role, department...")
    with col2:
        dept = st.selectbox("Department", ["All"] + list(set(e['department'] for e in st.session_state.employees)))
    with col3:
        if st.button("➕ Add Employee", type="primary"):
            st.info("Coming soon!")
    filtered = st.session_state.employees
    if search:
        filtered = [e for e in filtered if search.lower() in e['name'].lower() or search.lower() in e['role'].lower()]
    if dept != "All":
        filtered = [e for e in filtered if e['department'] == dept]
    cols = st.columns(2)
    for idx, emp in enumerate(filtered):
        with cols[idx % 2]:
            skills_html = ''.join([f'<span class="ibm-skill-tag">{s}</span>' for s in emp['skills'][:3]])
            st.markdown(f"""<div class="ibm-employee-card"><div style="display:flex;gap:1.5rem"><div class="ibm-avatar">{emp['name'][0]}</div><div style="flex:1"><h3 style="color:#064e3b;margin:0">{emp['name']}</h3><p style="color:#10b981;font-weight:600;margin:0.25rem 0">{emp['role']}</p><div style="display:flex;gap:0.5rem;margin:0.5rem 0"><span style="padding:4px 12px;background:linear-gradient(135deg,#d1fae5,#a7f3d0);color:#047857;border-radius:12px;font-size:12px;font-weight:600">{emp['status']}</span><span style="padding:4px 12px;background:#fef3c7;color:#92400e;border-radius:12px;font-size:12px">⭐ {emp['performance_score']}</span></div><p style="color:#6b7280;font-size:13px;margin:0.5rem 0">📧 {emp['email']} • 📍 {emp['location']}</p><div>{skills_html}</div></div></div></div>""", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.button("View Profile", key=f"v_{emp['id']}", use_container_width=True)
            with c2:
                st.button("Edit", key=f"e_{emp['id']}", use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)

# Recruitment
def show_recruitment():
    st.markdown(f"## 👥 Recruitment Hub {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]: st.metric("Open Positions", len(st.session_state.job_postings), "+3")
    with cols[1]: st.metric("Total Applications", sum(j['applications'] for j in st.session_state.job_postings), "+15")
    with cols[2]: st.metric("In Interview", len([c for c in st.session_state.candidates if 'Interview' in c['status']]), "+2")
    with cols[3]: st.metric("Avg. Time to Hire", "28 days", "-4")
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Job Postings", "🎯 Candidates", "✨ AI Tools", "📊 Pipeline"])
    with tab1:
        for job in st.session_state.job_postings:
            st.markdown(f"""<div class="ibm-feature-card"><h3 style="color:#064e3b;margin-bottom:0.5rem">{job['title']}</h3><div style="display:flex;gap:1rem;margin:0.5rem 0;flex-wrap:wrap"><span style="color:#6b7280">📍 {job['location']}</span><span style="color:#6b7280">💼 {job['type']}</span><span style="color:#6b7280">💰 {job['salary_range']}</span><span style="color:#6b7280">📅 {job['posted_date']}</span></div><div style="display:flex;gap:0.5rem"><span style="padding:4px 12px;background:linear-gradient(135deg,#d1fae5,#a7f3d0);color:#047857;border-radius:12px;font-size:12px;font-weight:600">{job['status']}</span><span style="padding:4px 12px;background:#dbeafe;color:#1e40af;border-radius:12px;font-size:12px">{job['applications']} Applications</span></div></div>""", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.button("View Details", key=f"jv_{job['id']}", use_container_width=True)
            with c2: st.button("View Applicants", key=f"ja_{job['id']}", use_container_width=True)
            with c3: st.button("Edit", key=f"je_{job['id']}", use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
    with tab2:
        for cand in st.session_state.candidates:
            skills_html = ''.join([f'<span class="ibm-skill-tag">{s}</span>' for s in cand['skills']])
            st.markdown(f"""<div class="ibm-feature-card"><div style="display:flex;gap:1.5rem"><div class="ibm-avatar" style="width:60px;height:60px;font-size:24px;background:linear-gradient(135deg,#f97316,#fb923c)">{cand['name'][0]}</div><div style="flex:1"><div style="display:flex;justify-content:space-between"><div><h4 style="color:#1e293b;margin:0">{cand['name']}</h4><p style="color:#10b981;font-weight:600">{cand['position_applied']}</p></div><div style="text-align:right"><div style="font-size:24px;font-weight:800;color:#10b981">{cand['score']}</div><div style="font-size:12px;color:#6b7280">AI Score</div></div></div><p style="color:#6b7280;font-size:13px">📧 {cand['email']} • 🎓 {cand['education']} • 💼 {cand['experience']}</p><div style="display:flex;gap:0.5rem;margin:0.5rem 0"><span style="padding:4px 12px;background:#fef3c7;color:#92400e;border-radius:12px;font-size:12px;font-weight:600">{cand['status']}</span></div><div>{skills_html}</div></div></div></div>""", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.button("View Resume", key=f"cr_{cand['id']}", use_container_width=True)
            with c2: st.button("Schedule Interview", key=f"cs_{cand['id']}", use_container_width=True)
            with c3: st.button("Advance", key=f"ca_{cand['id']}", use_container_width=True, type="primary")
            st.markdown("<br>", unsafe_allow_html=True)
    with tab3:
        st.markdown("### 🤖 AI-Powered Tools")
        tool_tabs = st.tabs(["📝 Job Description", "🎯 Resume Analyzer", "💬 Interview Questions"])
        with tool_tabs[0]:
            job_input = st.text_area("Job Details", placeholder="Enter job title and key requirements...", height=150)
            if st.button("✨ Generate Job Description", type="primary"):
                if job_input:
                    with st.spinner("🤖 Generating..."):
                        response = call_openrouter_api(f"Generate a job description for: {job_input}")
                        st.markdown(f"""<div class="ibm-response-container"><div class="ibm-response-header">✅ Generated Job Description</div><div class="ibm-response-content">{response}</div></div>""", unsafe_allow_html=True)
        with tool_tabs[1]:
            resume = st.text_area("Resume Content", placeholder="Paste resume text here...", height=200)
            if st.button("🔍 Analyze Resume", type="primary"):
                if resume:
                    with st.spinner("🤖 Analyzing..."):
                        response = call_openrouter_api(f"Analyze this resume: {resume}")
                        st.markdown(f"""<div class="ibm-response-container"><div class="ibm-response-header">✅ Resume Analysis</div><div class="ibm-response-content">{response}</div></div>""", unsafe_allow_html=True)
        with tool_tabs[2]:
            role = st.text_input("Role", placeholder="e.g., Senior Product Manager")
            interview_type = st.selectbox("Type", ["Technical", "Behavioral", "Leadership", "Cultural Fit"])
            if st.button("🎤 Generate Questions", type="primary"):
                if role:
                    with st.spinner("🤖 Creating..."):
                        response = call_openrouter_api(f"Generate {interview_type} interview questions for {role}")
                        st.markdown(f"""<div class="ibm-response-container"><div class="ibm-response-header">✅ Interview Questions</div><div class="ibm-response-content">{response}</div></div>""", unsafe_allow_html=True)
    with tab4:
        st.markdown("### 📊 Recruitment Pipeline")
        stages = {"📨 New": 12, "📞 Screen": 8, "💻 Technical": 5, "👔 Final": 3, "✅ Offer": 2}
        cols = st.columns(len(stages))
        for col, (stage, count) in zip(cols, stages.items()):
            with col:
                st.markdown(f"""<div class="ibm-kanban-column"><h4 style="color:#064e3b">{stage}</h4><div style="text-align:center;font-size:32px;font-weight:800;color:#10b981">{count}</div></div>""", unsafe_allow_html=True)

# Onboarding
def show_onboarding():
    st.markdown(f"## 📋 Onboarding {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🚀 Create Plan", "📊 Active Plans"])
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            role = st.text_input("New Hire Role", placeholder="e.g., Marketing Manager")
            dept = st.selectbox("Department", ["Engineering", "Marketing", "Sales", "HR", "Finance", "Product"])
            start = st.date_input("Start Date")
            if st.button("✨ Generate Onboarding Plan", type="primary"):
                if role:
                    with st.spinner("🤖 Creating plan..."):
                        response = call_openrouter_api(f"Create 30-day onboarding plan for {role} in {dept}")
                        st.markdown(f"""<div class="ibm-response-container"><div class="ibm-response-header">✅ Onboarding Plan</div><div class="ibm-response-content">{response}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.info("**📌 Best Practices:**\n\n• Start before day one\n• Set clear 30-60-90 goals\n• Assign a buddy\n• Regular check-ins\n• Gather feedback")
    with tab2:
        st.markdown("### 📊 Active Onboarding")
        onboarding_data = [("Sarah Johnson", "Software Engineer", "Week 2", 45), ("Michael Chen", "Marketing Manager", "Week 1", 20)]
        for name, role, week, progress in onboarding_data:
            st.markdown(f"""<div class="ibm-feature-card"><h4 style="color:#064e3b">{name}</h4><p style="color:#6b7280">{role} • {week}</p><div class="ibm-progress-container"><div class="ibm-progress-bar" style="width:{progress}%"></div></div><p style="color:#10b981;font-size:13px;margin-top:0.5rem">{progress}% complete</p></div>""", unsafe_allow_html=True)

# Performance
def show_performance():
    st.markdown(f"## 🎯 Performance Management {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]: st.metric("Reviews Due", "45", "15 this week")
    with cols[1]: st.metric("Avg Score", "4.2/5", "+0.3")
    with cols[2]: st.metric("Goals Met", "78%", "+5%")
    with cols[3]: st.metric("Top Performers", "23", "+4")
    tab1, tab2, tab3 = st.tabs(["📝 Create Review", "🎯 Goals", "📊 Analytics"])
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            emp_name = st.text_input("Employee Name")
            position = st.text_input("Position")
            period = st.selectbox("Review Period", ["Q1 2024", "Q2 2024", "Annual 2024"])
            strengths = st.text_area("Strengths & Achievements", height=100)
            improvements = st.text_area("Areas for Development", height=100)
            if st.button("✨ Generate Review", type="primary"):
                if emp_name:
                    with st.spinner("🤖 Creating review..."):
                        response = call_openrouter_api(f"Create performance review for {emp_name}, {position}. Strengths: {strengths}. Development: {improvements}")
                        st.markdown(f"""<div class="ibm-response-container"><div class="ibm-response-header">✅ Performance Review</div><div class="ibm-response-content">{response}</div></div>""", unsafe_allow_html=True)
    with tab2:
        st.markdown("### 🎯 Team Goals")
        for goal in st.session_state.goals:
            st.markdown(f"""<div class="ibm-feature-card"><h4 style="color:#064e3b">{goal['title']}</h4><p style="color:#6b7280">{goal['owner']} • Due: {goal['due']}</p><div class="ibm-progress-container"><div class="ibm-progress-bar" style="width:{goal['progress']}%"></div></div><p style="color:#10b981;font-size:13px;margin-top:0.5rem">{goal['progress']}% complete</p></div>""", unsafe_allow_html=True)
    with tab3:
        st.markdown("### 📊 Performance Analytics")
        st.markdown("""<div class="ibm-feature-card"><h4>Department Performance</h4><p>Engineering: ⭐ 4.5 | Marketing: ⭐ 4.2 | Sales: ⭐ 4.8 | HR: ⭐ 4.0</p></div>""", unsafe_allow_html=True)

# Training
def show_training():
    st.markdown(f"## 🎓 Training & Development {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]: st.metric("Active Courses", "24")
    with cols[1]: st.metric("Completion Rate", "78%", "+8%")
    with cols[2]: st.metric("Hours Trained", "1,256", "+156")
    with cols[3]: st.metric("Certifications", "45", "+12")
    tab1, tab2 = st.tabs(["📚 Learning Paths", "🎯 Skills Gap"])
    with tab1:
        current = st.text_input("Current Role", placeholder="e.g., Junior Developer")
        target = st.text_input("Target Role", placeholder="e.g., Senior Developer")
        timeline = st.selectbox("Timeline", ["3 months", "6 months", "1 year"])
        if st.button("🚀 Generate Learning Path", type="primary"):
            if current and target:
                with st.spinner("🤖 Creating path..."):
                    response = call_openrouter_api(f"Create learning path from {current} to {target} in {timeline}")
                    st.markdown(f"""<div class="ibm-response-container"><div class="ibm-response-header">✅ Learning Path</div><div class="ibm-response-content">{response}</div></div>""", unsafe_allow_html=True)
    with tab2:
        current_skills = st.text_area("Current Skills", height=100)
        required = st.text_area("Required Skills", height=100)
        if st.button("🔍 Analyze Gap", type="primary"):
            if current_skills:
                response = call_openrouter_api(f"Analyze skills gap. Current: {current_skills}. Required: {required}")
                st.markdown(f"""<div class="ibm-response-container"><div class="ibm-response-header">✅ Skills Gap Analysis</div><div class="ibm-response-content">{response}</div></div>""", unsafe_allow_html=True)

# Payroll
def show_payroll():
    st.markdown(f"## 💰 Payroll {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]: st.metric("Monthly Payroll", "$498K")
    with cols[1]: st.metric("Avg Salary", "$95K")
    with cols[2]: st.metric("Benefits Cost", "$74.7K")
    with cols[3]: st.metric("Tax Withholding", "$124.5K")
    st.markdown("### 📊 Payroll Summary")
    for data in st.session_state.payroll_data:
        st.markdown(f"""<div class="ibm-feature-card"><h4 style="color:#064e3b">{data['month']} 2024</h4><div style="display:flex;gap:2rem"><div><span style="color:#6b7280">Gross:</span> <b>${data['total']:,}</b></div><div><span style="color:#6b7280">Taxes:</span> <b>${data['taxes']:,}</b></div><div><span style="color:#6b7280">Benefits:</span> <b>${data['benefits']:,}</b></div><div><span style="color:#10b981">Net:</span> <b>${data['net']:,}</b></div></div></div>""", unsafe_allow_html=True)

# Benefits
def show_benefits():
    st.markdown(f"## 🏥 Benefits {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    data = st.session_state.benefits_data
    cols = st.columns(4)
    with cols[0]: st.metric("Health Enrollment", f"{data['health_enrollment']}%")
    with cols[1]: st.metric("401(k) Participation", f"{data['401k_participation']}%")
    with cols[2]: st.metric("Avg 401(k) Contribution", f"{data['avg_401k_contribution']}%")
    with cols[3]: st.metric("HSA Enrollment", f"{data['hsa_enrollment']}%")
    st.markdown("### 📊 Enrollment Overview")
    benefits_list = [("🏥 Health Insurance", data['health_enrollment']), ("🦷 Dental", data['dental_enrollment']), ("👁️ Vision", data['vision_enrollment']), ("💰 401(k)", data['401k_participation'])]
    for name, pct in benefits_list:
        st.markdown(f"**{name}**")
        st.markdown(f"""<div class="ibm-progress-container"><div class="ibm-progress-bar" style="width:{pct}%"></div></div>""", unsafe_allow_html=True)
        st.caption(f"{pct}% enrolled")

# Time & Leave
def show_time_leave():
    st.markdown(f"## 📅 Time & Leave {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]: st.metric("Pending Requests", "8")
    with cols[1]: st.metric("Approved This Month", "23")
    with cols[2]: st.metric("Avg Days/Employee", "15.2")
    with cols[3]: st.metric("Utilization", "78%")
    st.markdown("### 📋 Leave Requests")
    requests = [("Sarah Johnson", "Vacation", "Feb 10-14", "Pending"), ("Michael Chen", "Sick Leave", "Feb 8", "Approved"), ("Emily Davis", "Personal", "Feb 15", "Pending")]
    for name, type_, dates, status in requests:
        color = "#d1fae5" if status == "Approved" else "#fef3c7"
        st.markdown(f"""<div class="ibm-feature-card"><div style="display:flex;justify-content:space-between;align-items:center"><div><h4 style="color:#064e3b;margin:0">{name}</h4><p style="color:#6b7280;margin:0">{type_} • {dates}</p></div><span style="padding:4px 12px;background:{color};border-radius:12px;font-size:12px;font-weight:600">{status}</span></div></div>""", unsafe_allow_html=True)

# Compliance
def show_compliance():
    st.markdown(f"## ✅ Compliance {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]: st.metric("Compliance Score", "94%")
    with cols[1]: st.metric("Completed", "12/15")
    with cols[2]: st.metric("Action Required", "2")
    with cols[3]: st.metric("Upcoming Audits", "1")
    st.markdown("### 📋 Compliance Items")
    for item in st.session_state.compliance_data:
        color = "#d1fae5" if item['status'] == "Compliant" else "#fef3c7" if item['status'] == "In Progress" else "#fee2e2"
        st.markdown(f"""<div class="ibm-feature-card"><div style="display:flex;justify-content:space-between;align-items:center"><div><h4 style="color:#064e3b;margin:0">{item['item']}</h4><p style="color:#6b7280;margin:0">Due: {item['due']}</p></div><span style="padding:4px 12px;background:{color};border-radius:12px;font-size:12px;font-weight:600">{item['status']}</span></div><div class="ibm-progress-container" style="margin-top:1rem"><div class="ibm-progress-bar" style="width:{item['completion']}%"></div></div></div>""", unsafe_allow_html=True)

# Analytics
def show_analytics():
    st.markdown(f"## 📊 Analytics {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    cols = st.columns(5)
    metrics = [("Headcount", "1,234", "+5.2%"), ("Growth", "12%", "+2%"), ("Avg Salary", "$95K", "+3.5%"), ("Satisfaction", "8.4/10", "+0.3"), ("Retention", "94%", "+2%")]
    for col, (label, value, delta) in zip(cols, metrics):
        with col: st.metric(label, value, delta)
    st.markdown("### 📄 Generate Report")
    report_type = st.selectbox("Report Type", ["Workforce Demographics", "Recruitment Metrics", "Performance Summary", "Compensation Analysis", "Turnover Report"])
    period = st.selectbox("Period", ["Last Month", "Last Quarter", "Last Year"])
    if st.button("📊 Generate Report", type="primary"):
        with st.spinner("🤖 Generating..."):
            response = call_openrouter_api(f"Create {report_type} report for {period}")
            st.markdown(f"""<div class="ibm-response-container"><div class="ibm-response-header">✅ Report</div><div class="ibm-response-content">{response}</div></div>""", unsafe_allow_html=True)

# Documents
def show_documents():
    st.markdown(f"## 📝 Documents {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1: search = st.text_input("🔍 Search documents", placeholder="Search...")
    with col2: st.button("➕ Upload", type="primary", use_container_width=True)
    for doc in st.session_state.documents:
        st.markdown(f"""<div class="ibm-feature-card"><div style="display:flex;justify-content:space-between;align-items:center"><div><h4 style="color:#064e3b;margin:0">📄 {doc['name']}</h4><p style="color:#6b7280;margin:0">{doc['type']} • Updated: {doc['updated']} • {doc['size']}</p></div><div><button style="background:linear-gradient(135deg,#10b981,#34d399);color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer">Download</button></div></div></div>""", unsafe_allow_html=True)

# Announcements
def show_announcements():
    st.markdown(f"## 📣 Announcements {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    if st.button("➕ New Announcement", type="primary"):
        st.info("Announcement form coming soon!")
    for ann in st.session_state.announcements:
        priority_color = "#fee2e2" if ann['priority'] == 'high' else "#fef3c7"
        st.markdown(f"""<div class="ibm-feature-card"><h3 style="color:#064e3b">{ann['title']}</h3><div style="display:flex;gap:1rem;align-items:center"><span style="color:#6b7280">📅 {ann['date']}</span><span style="padding:4px 12px;background:{priority_color};border-radius:12px;font-size:12px;font-weight:600;text-transform:uppercase">{ann['priority']}</span></div></div>""", unsafe_allow_html=True)

# AI Assistant
def show_ai_assistant():
    st.markdown(f"## 💬 AI Assistant {'<span class=\"ibm-demo-badge\">DEMO</span>' if st.session_state.demo_mode else ''}", unsafe_allow_html=True)
    st.markdown("### 💡 Try these prompts:")
    prompts = ["Generate a job description for Data Scientist", "Create onboarding plan for new Marketing Manager", "Interview questions for Product Manager", "Write a remote work policy", "Performance review template"]
    cols = st.columns(3)
    for idx, prompt in enumerate(prompts[:3]):
        with cols[idx]:
            if st.button(prompt, key=f"p_{idx}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                response = call_openrouter_api(prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
    st.markdown("---")
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation")
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"""<div style="display:flex;justify-content:flex-end;margin:1rem 0"><div class="ibm-chat-bubble-user">{msg['content']}</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="display:flex;justify-content:flex-start;margin:1rem 0"><div class="ibm-chat-bubble-assistant">{msg['content']}</div></div>""", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Ask me anything about HR...", placeholder="Type your question...", label_visibility="collapsed", key="ai_input")
    with col2:
        if st.button("Send 🚀", type="primary", use_container_width=True):
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("🤖 Thinking..."):
                    response = call_openrouter_api(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

# Main Application
def main():
    init_session_state()
    if not st.session_state.authenticated:
        show_auth_page()
        return
    show_sidebar()
    pages = {"Dashboard": show_dashboard, "Recruitment": show_recruitment, "Onboarding": show_onboarding, "Employee Directory": show_employee_directory, "Performance": show_performance, "Training": show_training, "Payroll": show_payroll, "Benefits": show_benefits, "Time & Leave": show_time_leave, "Compliance": show_compliance, "Analytics": show_analytics, "Documents": show_documents, "Announcements": show_announcements, "AI Assistant": show_ai_assistant}
    page_func = pages.get(st.session_state.current_page, show_dashboard)
    page_func()
    st.markdown("""<div class="ibm-footer"><p><span class="ibm-footer-brand">TalentPilot</span> - AI-Powered HR Orchestration Platform</p><p style="margin-top:0.5rem">Built with ❤️ by <b>cybe4sent1nel (FAHAD KHAN)</b></p><p style="margin-top:0.5rem">🎮 {'Demo Mode Active' if st.session_state.demo_mode else 'Connected'}</p></div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
