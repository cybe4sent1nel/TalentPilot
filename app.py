# TalentPilot HR Orchestration Platform
# Streamlit App - UI Refactor: FAHAD KHAN (Powered by IBM watsonx), Purple-Green-Black color scheme, Material Icons, and branding

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time
import random
import base64
from io import BytesIO
import calendar
import os

# ================= GLOBAL CONFIG & THEME SETUP ================
st.set_page_config(
    page_title="TalentPilot - AI HR Orchestration",
    layout="wide",
    page_icon="🦄",  # Will be replaced in branding
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS FOR THE WHOLE APP ================
st.markdown("""
<style>
body { background-color: #232323; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #7D3C98 40%, #222 100%) !important;
    border-right: 4px solid #26A65B !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: #fff; }
.main {
    background: linear-gradient(135deg, #efeafe 0%, #222 35%, #151e11 100%);
    background-attachment: fixed;
}
.material-icons {
    font-family: 'Material Icons';
    font-weight: normal;
    font-style: normal;
    font-size: 24px;
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
}
.logo-container {
    display: flex; align-items: center; justify-content: center;
    padding: 2rem 1rem; margin-bottom: 1.5rem;
    border-bottom: 2px solid rgba(44,255,173,0.12);
    background: linear-gradient(135deg, #7D3C98 20%, #26A65B 100%);
    border-radius: 0 0 30px 30px;
}
.logo-box {
    width: 80px; height: 80px;
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 6px 28px #26A65B44;
    transition: all 0.3s ease;
    overflow: hidden;
    background: #fff;
}
.logo-box img { width: 100%; height: 100%; object-fit: contain; }
.logo-text {
    margin-left: 1.2rem; font-size: 34px; font-weight: 800;
    background: linear-gradient(90deg,#7D3C98,#26A65B);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -1.2px;
}
.slogan {
    margin-left: 1rem; color: #c8ffe9; font-size: 15px; font-weight: 500;
    text-shadow:0 0 4px #232;
}
.sidebar-credit {
    margin-top:2.2rem;
    padding:1.1rem 0.8rem 0.8rem 0.8rem;
    background:rgba(20,18,34,0.95);
    border: 2px solid #26A65B77;
    color: #fff;
    border-radius: 15px;
    text-align:center;
    font-size: 1rem;
    font-weight:600;
    line-height:1.6;
}
.nav-btn {
    background-image: linear-gradient(90deg,#211c23 70%, #233 110%);
    color:#fff;
    border:none;
    border-radius: 10px;
    width:100%;
    font-size:1.08rem;
    font-weight:600;
    padding:12px 19px;
    margin-bottom:12px;
    display:flex;
    align-items:center;
    gap: 14px;
    cursor:pointer;
    transition:.16s;
    box-shadow: 0px 3px 12px #2223;
}
.nav-btn:hover { background: linear-gradient(90deg,#26A65B77,#7D3C9877) !important; color:#fff; }
</style>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

# ================= LOGO & BRANDING SECTION ================
with st.sidebar:
    st.markdown(
        f"""
        <div class="logo-container">
            <div class="logo-box">
                <img src="data:image/png;base64,{base64.b64encode(open('Gemini_Generated_Image_ra57c5ra57c5ra57.jpg','rb').read()).decode()}" alt="Logo">
            </div>
            <div>
                <div class="logo-text">TALENTPILOT</div>
                <span class="slogan">Orchestrate HR Agent</span>
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown(
        "<div class='sidebar-credit'>Developer: FAHAD KHAN<br>Powered by IBM watsonx</div>",
        unsafe_allow_html=True
    )

    # Navigation buttons
    pages = [
        ("Dashboard", "dashboard"),
        ("Employee Directory", "group"),
        ("Recruitment", "business_center"),
        ("Performance", "trending_up"),
        ("Onboarding", "how_to_reg"),
        ("Payroll", "payments"),
        ("Benefits", "health_and_safety"),
        ("Compliance", "verified"),
        ("Analytics", "analytics"),
        ("Documents", "description"),
        ("AI Assistant", "smart_toy")
    ]
    st.markdown("<br>", unsafe_allow_html=True)
    nav_choice = st.radio(
        "Go to", [f"{label}" for label, _ in pages],
        label_visibility="collapsed"
    )

# ======================= NEXT: DASHBOARD & DATA =======================
# (Say "next" to get the next full section. All code and features will be provided!)
# ================== DATA GENERATORS AND DEMO MODE MOCKUPS ==================
# Modular functions for generating sample HR, recruitment and analytics data

def generate_sample_employees():
    # Replace with actual DB/API integration for production!
    return [
        {'id': 'EMP001', 'name': 'Sarah Johnson', 'role': 'Senior Software Engineer', 'department': 'Engineering', 'email': 'sarah.j@company.com', 'phone': '+1 (555) 123-4567', 'hire_date': '2021-03-15', 'salary': 125000, 'status': 'Active', 'manager': 'John Smith', 'location': 'San Francisco, CA', 'skills': ['Python', 'React', 'AWS', 'Docker'], 'performance_score': 4.5, 'pto_balance': 15, 'team': 'Platform'},
        {'id': 'EMP002', 'name': 'Michael Chen', 'role': 'Marketing Manager', 'department': 'Marketing', 'email': 'michael.c@company.com', 'phone': '+1 (555) 234-5678', 'hire_date': '2020-07-20', 'salary': 95000, 'status': 'Active', 'manager': 'Lisa Wong', 'location': 'New York, NY', 'skills': ['SEO', 'Content Strategy', 'Analytics'], 'performance_score': 4.2, 'pto_balance': 12, 'team': 'Growth'},
        {'id': 'EMP003', 'name': 'Emily Davis', 'role': 'Sales Director', 'department': 'Sales', 'email': 'emily.d@company.com', 'phone': '+1 (555) 345-6789', 'hire_date': '2019-01-10', 'salary': 135000, 'status': 'Active', 'manager': 'Robert Brown', 'location': 'Chicago, IL', 'skills': ['Sales Strategy', 'CRM', 'Negotiation'], 'performance_score': 4.8, 'pto_balance': 8, 'team': 'Enterprise'},
    ]

def generate_sample_jobs():
    return [
        {'id': 'JOB001', 'title': 'Senior Full-Stack Developer', 'department': 'Engineering', 'location': 'Remote', 'type': 'Full-time', 'salary_range': '$120k - $160k', 'posted_date': '2024-01-15', 'applications': 45, 'status': 'Open', 'description': 'Looking for an experienced full-stack developer...'},
        {'id': 'JOB002', 'title': 'Product Manager', 'department': 'Product', 'location': 'San Francisco, CA', 'type': 'Full-time', 'salary_range': '$130k - $170k', 'posted_date': '2024-01-20', 'applications': 32, 'status': 'Open', 'description': 'Seeking a strategic product manager...'},
    ]

def generate_sample_candidates():
    return [
        {'id': 'CAN001', 'name': 'Alex Thompson', 'email': 'alex.t@email.com', 'phone': '+1 (555) 111-2222', 'position_applied': 'Senior Full-Stack Developer', 'status': 'Phone Screen', 'score': 85, 'experience': '7 years', 'education': 'BS Computer Science', 'skills': ['React', 'Node.js', 'PostgreSQL', 'AWS'], 'applied_date': '2024-01-16', 'interview_date': '2024-02-05'},
        {'id': 'CAN002', 'name': 'Jordan Lee', 'email': 'jordan.l@email.com', 'phone': '+1 (555) 222-3333', 'position_applied': 'Product Manager', 'status': 'Technical Interview', 'score': 92, 'experience': '5 years', 'education': 'MBA + BS Engineering', 'skills': ['Product Strategy', 'Agile', 'Data Analysis'], 'applied_date': '2024-01-21', 'interview_date': '2024-02-08'},
    ]

# ...[insert other sample generator functions as needed]...

# Initialize session state data at runtime
def init_session_state():
    defaults = {
        'authenticated': False, 'api_key': '', 'demo_mode': False, 'current_page': 'Dashboard',
        'employees': generate_sample_employees(), 'job_postings': generate_sample_jobs(),
        'candidates': generate_sample_candidates(),
        'user_name': 'HR Manager', 'company_name': 'TechCorp Inc.', 'employee_count': 1234,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ================= DASHBOARD SECTION ======================
def show_dashboard():
    # Cards and metrics use Material Icons, purple/green accents
    st.markdown("""
    <div style='margin-top:16px;margin-bottom:10px;'>
        <h2 style='color:#7D3C98;font-size:2.2rem;font-weight:800;margin-bottom:6px;'>HR Dashboard</h2>
    </div>""", unsafe_allow_html=True)

    metrics = [
        ("Employees", "group", st.session_state.employee_count, "#7D3C98"),
        ("Open Roles", "business_center", len(st.session_state.job_postings), "#26A65B"),
        ("Reviews Due", "trending_up", 12, "#7D3C98"),
        ("Active Training", "school", 78, "#26A65B"),
        ("eNPS Score", "emoji_events", 8.4, "#7D3C98"),
    ]
    metric_cols = st.columns(len(metrics))
    for col, (label, icon, val, color) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f"<div class='metric-card'><span class='material-icons metric-icon' style='color:{color};'>{icon}</span>"
                f"<div><div style='font-size:1.6rem;font-weight:700;'>{val}</div><div>{label}</div></div></div>",
                unsafe_allow_html=True
            )

    st.write("Welcome to TalentPilot. All your HR metrics and navigation are here. Choose a module from the sidebar to continue.")

# =================== SECTION ROUTER ======================
if nav_choice == "Dashboard":
    show_dashboard()

# Next: Employee Directory, Recruitment, and remaining HR features
# Reply “next” for the following sections!
# ================ EMPLOYEE DIRECTORY ================
def show_employee_directory():
    st.markdown("""
    <h2 style='color:#26A65B;font-weight:800;margin-top:4px;margin-bottom:10px;'>Employee Directory</h2>
    """, unsafe_allow_html=True)
    search = st.text_input("Search employees", placeholder="Enter name, role, or department...")
    filtered = st.session_state.employees
    if search:
        filtered = [e for e in filtered if search.lower() in e['name'].lower() or search.lower() in e['role'].lower() or search.lower() in e['department'].lower()]
    cols = st.columns(2)
    for idx, emp in enumerate(filtered):
        with cols[idx % 2]:
            skills_html = ''.join([f'<span style="color:#26A65B;font-size:13px;margin-right:8px;">{s}</span>' for s in emp['skills'][:3]])
            st.markdown(
                f"""
                <div style='background:#fff;border-radius:18px;padding:18px 22px;margin-bottom:18px;box-shadow:0 4px 18px #2222;'>
                    <div style='display:flex;align-items:center;'>
                        <span class="material-icons metric-icon" style="color:#7D3C98;font-size:2.3rem;margin-right:16px;">person</span>
                        <div>
                            <div style="font-size:1.25rem;font-weight:700;color:#222">{emp['name']}</div>
                            <div style="font-size:1.07rem;color:#26A65B;font-weight:600;">{emp['role']}</div>
                            <div style="font-size:13px;color:#151e11;">{emp['email']} | {emp['location']}</div>
                            <div style="margin-top:8px;">{skills_html}</div>
                            <div style="margin-top:6px;font-size:13px;">
                                <span style="color:#7D3C98;">Manager:</span> {emp['manager']} | <span style="color:#7D3C98;">Status:</span> {emp['status']}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True
            )

    st.button("Add Employee", key="add_emp_btn")

# ================ RECRUITMENT HUB ================
def show_recruitment():
    st.markdown("""
    <h2 style='color:#7D3C98;font-weight:800;margin-top:4px;margin-bottom:10px;'>Recruitment Hub</h2>
    """, unsafe_allow_html=True)
    st.write("Open positions in your organization and application statistics.")
    job_cols = st.columns(2)
    for idx, job in enumerate(st.session_state.job_postings):
        with job_cols[idx % 2]:
            st.markdown(
                f"""
                <div style='background:#fff;border-radius:16px;padding:18px 20px;margin-bottom:18px;box-shadow:0 3px 12px #7D3C9833;'>
                    <div style='display:flex;align-items:center;margin-bottom:7px;'>
                        <span class="material-icons metric-icon" style="color:#26A65B;font-size:2.1rem;margin-right:14px;">business_center</span>
                        <div style='font-size:1.13rem;font-weight:700;color:#7D3C98'>{job['title']}</div>
                    </div>
                    <div style='font-size:13px;color:#222;margin-bottom:4px;'>Dept: {job['department']} | Location: {job['location']}</div>
                    <div style='font-size:13px;color:#151e11;margin-bottom:4px;'>Salary: {job['salary_range']} | Posted: {job['posted_date']}</div>
                    <div style='font-size:13px;color:#222;margin-bottom:4px;'>Applications: <span style="color:#26A65B;font-weight:700;">{job['applications']}</span></div>
                    <div style='font-size:13px;color:#26A65B;margin-bottom:4px;'>Status: {job['status']}</div>
                    <button class='nav-btn' style='margin-top:12px;width:70%;'><span class='material-icons'>visibility</span>View Details</button>
                </div>
                """, unsafe_allow_html=True
            )
    st.button("Post New Job", key="post_job_btn")

# ================ CANDIDATE MANAGEMENT ================
def show_candidates():
    st.markdown("""
    <h2 style='color:#26A65B;font-weight:800;margin-top:4px;margin-bottom:10px;'>Candidate Pipeline</h2>
    """, unsafe_allow_html=True)
    candidates = st.session_state.candidates
    for cand in candidates:
        st.markdown(
            f"""
            <div style='background:#fff;border-radius:18px;padding:15px 18px;margin-bottom:14px;box-shadow:0 4px 18px #2222;'>
                <div style='display:flex;align-items:center;'>
                    <span class="material-icons metric-icon" style="color:#7D3C98;font-size:2rem;margin-right:13px;">person_search</span>
                    <div style='font-size:1.15rem;font-weight:700;color:#222'>{cand['name']}</div>
                </div>
                <div style="font-size:13px;color:#151e11;">Applied for: <b>{cand['position_applied']}</b> | Status: <b style="color:#26A65B;">{cand['status']}</b></div>
                <div style="font-size:13px;color:#7D3C98;">Score: {cand['score']} | Interview: {cand['interview_date']}</div>
                <div style='margin-top:10px;'>
                    <button class='nav-btn' style='width:48%;margin-right:6px;'><span class='material-icons'>description</span>View Resume</button>
                    <button class='nav-btn' style='width:48%;'><span class='material-icons'>calendar_month</span>Schedule Interview</button>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

# ================ ONBOARDING MANAGER ================
def show_onboarding():
    st.markdown("""
    <h2 style='color:#7D3C98;font-weight:800;margin-top:4px;margin-bottom:10px;'>Onboarding Manager</h2>
    """, unsafe_allow_html=True)
    st.write("Generate onboarding plans and manage new hires.")
    role = st.text_input("Role", placeholder="e.g., Engineer")
    dept = st.text_input("Department", placeholder="e.g., Engineering")
    start = st.date_input("Start Date")
    if st.button("Generate Onboarding Plan"):
        st.success(f"30-day onboarding plan generated for {role} in {dept} starting {start}")

# =============================== ROUTER (CONTINUED) ===============================
if nav_choice == "Employee Directory":
    show_employee_directory()
elif nav_choice == "Recruitment":
    show_recruitment()
elif nav_choice == "AI Assistant":  # (Handled in later sections)
    pass

# Next: Performance, Payroll, Benefits, Compliance, Analytics, Documents, AI Assistant
# Say "next" for remaining modules!
# ================ PERFORMANCE MANAGEMENT ================
def show_performance():
    st.markdown("""
    <h2 style='color:#26A65B;font-weight:800;margin-top:4px;margin-bottom:10px;'>Performance Reviews</h2>
    """, unsafe_allow_html=True)
    # Display table for reviews - add field editing/AI features as necessary
    st.write("Current performance reviews in your organization.")
    review_data = [
        {"Employee": "Sarah Johnson", "Score": 4.8, "Feedback": "Excellent teamwork & leadership."},
        {"Employee": "Michael Chen", "Score": 4.3, "Feedback": "Creative, strong market insights."},
        {"Employee": "Emily Davis", "Score": 4.7, "Feedback": "Consistent sales growth, great morale."},
    ]
    st.dataframe(review_data, use_container_width=True)
    emp = st.text_input("Review for Employee (Name)")
    score = st.slider("Score", 1.0, 5.0, 4.0, 0.1)
    feedback = st.text_area("Feedback / Achievements")
    if st.button("Submit Performance Review"):
        st.success(f"Review for {emp} submitted successfully!")

# ================ PAYROLL SECTION ================
def show_payroll():
    st.markdown("""
    <h2 style='color:#7D3C98;font-weight:800;margin-top:4px;margin-bottom:10px;'>Payroll Summary</h2>
    """, unsafe_allow_html=True)
    st.metric("Total Payroll (monthly)", "$480,000")
    st.metric("Avg Salary", "$92,500")
    st.metric("Tax Withholding", "$41,800")
    st.metric("Benefits", "$43,000")
    st.button("Download Payslip")

# ================ BENEFITS =====================
def show_benefits():
    st.markdown("""
    <h2 style='color:#26A65B;font-weight:800;margin-top:4px;margin-bottom:10px;'>Benefits Center</h2>
    """, unsafe_allow_html=True)
    st.metric("Health Insurance", "92% Enrolled")
    st.metric("Dental Insurance", "85% Enrolled")
    st.metric("401(k)", "77% Participating")
    st.button("View Benefit Options")

# ================ COMPLIANCE =====================
def show_compliance():
    st.markdown("""
    <h2 style='color:#7D3C98;font-weight:800;margin-top:4px;margin-bottom:10px;'>Compliance Center</h2>
    """, unsafe_allow_html=True)
    compliance_data = [
        {"Policy": "I-9 Verification", "Due": "2025-02-03", "Status": "Compliant"},
        {"Policy": "OSHA Training", "Due": "2025-03-11", "Status": "In Progress"},
        {"Policy": "Data Privacy", "Due": "2025-02-15", "Status": "Compliant"},
        {"Policy": "Harassment Prevention", "Due": "2025-04-20", "Status": "Required"},
    ]
    st.dataframe(compliance_data, use_container_width=True)
    st.button("View All Policies")

# ================ ANALYTICS =====================
def show_analytics():
    st.markdown("""
    <h2 style='color:#26A65B;font-weight:800;margin-top:4px;margin-bottom:10px;'>Analytics Dashboard</h2>
    """, unsafe_allow_html=True)
    st.metric("Employee Retention", "93%")
    st.metric("Diversity Ratio", "54% Female, 46% Male")
    st.metric("Avg Tenure", "3.1 years")
    st.button("Download Analytics Report")

# ================ DOCUMENT MANAGEMENT ================
def show_documents():
    st.markdown("""
    <h2 style='color:#7D3C98;font-weight:800;margin-top:4px;margin-bottom:10px;'>HR Documents</h2>
    """, unsafe_allow_html=True)
    docs_demo = [
        {"Doc": "Employee Handbook 2025", "LastUpdated": "2025-01-12"},
        {"Doc": "Leave Policy", "LastUpdated": "2025-01-20"},
        {"Doc": "Remote Work Guide", "LastUpdated": "2025-02-02"},
    ]
    st.dataframe(docs_demo, use_container_width=True)
    st.button("Upload Document")
    st.button("Download")

# ================ AI ASSISTANT ================
def show_ai_assistant():
    st.markdown("""
    <h2 style='color:#7D3C98;font-weight:800;margin-top:4px;margin-bottom:10px;'>AI HR Assistant</h2>
    """, unsafe_allow_html=True)
    st.write("Get instant HR insights, generate documents, analyze resumes, or build job descriptions powered by AI.")
    prompt = st.text_area("Type your prompt/question to the AI Assistant", height=130)
    if st.button("Send to IBM watsonx"):
        st.success("This is a demo. Integrate AI backend/IBM watsonx here for real-time answers!")
        st.write("Example Output: 'AI-generated job description for Data Scientist...'")

# ================ ROUTER FOR REMAINING MODULES ================
if nav_choice == "Performance":
    show_performance()
elif nav_choice == "Payroll":
    show_payroll()
elif nav_choice == "Benefits":
    show_benefits()
elif nav_choice == "Compliance":
    show_compliance()
elif nav_choice == "Analytics":
    show_analytics()
elif nav_choice == "Documents":
    show_documents()
elif nav_choice == "AI Assistant":
    show_ai_assistant()

# ================ FOOTER / CREDITS ================
st.markdown(
    "<div class='footer-credit'>TalentPilot &copy; 2025 | Developer: FAHAD KHAN &mdash; Powered by IBM watsonx</div>",
    unsafe_allow_html=True
)
