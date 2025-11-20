import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
from openai import OpenAI
import time
import base64
import json
from datetime import datetime, timedelta
import random

# --- CONFIGURATION ---
st.set_page_config(
    page_title="TalentPilot | AI HR Orchestration",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME & STYLING ---
COLOR_PRIMARY = "#1E3A8A"  # Deep Blue
COLOR_SECONDARY = "#F97316"  # Vibrant Orange
COLOR_BG = "#F8FAFC"
COLOR_SUCCESS = "#10B981"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600&display=swap');
    
    /* Global Reset */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: {COLOR_BG};
        color: #1e293b;
    }}
    
    h1, h2, h3 {{
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: {COLOR_PRIMARY};
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: white;
        border-right: 1px solid #e2e8f0;
    }}
    
    /* Custom Cards (Glassmorphism-lite) */
    .tp-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #f1f5f9;
        margin-bottom: 1.5rem;
        transition: transform 0.2s;
    }}
    .tp-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }}
    
    /* Metrics Card */
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLOR_PRIMARY};
    }}
    .metric-label {{
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Primary Button */
    .stButton>button {{
        background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(30, 58, 138, 0.2);
        transition: all 0.2s;
    }}
    .stButton>button:hover {{
        box-shadow: 0 6px 8px rgba(30, 58, 138, 0.3);
        transform: translateY(-1px);
    }}

    /* Secondary/Action Button */
    .action-btn {{
        background-color: {COLOR_SECONDARY};
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        text-decoration: none;
        display: inline-block;
    }}

    /* Chat Interface */
    .chat-container {{
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e2e8f0;
        height: 400px;
        overflow-y: auto;
    }}
    
    /* Login Screen */
    .login-container {{
        max-width: 450px;
        margin: 10vh auto;
        padding: 3rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        text-align: center;
        border-top: 5px solid {COLOR_SECONDARY};
    }}
    </style>
""", unsafe_allow_html=True)

# --- ASSETS ---
def get_logo_svg(width=120):
    """Generates the TalentPilot Compass Logo."""
    svg = f"""
    <svg width="{width}" height="{width}" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#1E3A8A;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#2563eb;stop-opacity:1" />
        </linearGradient>
      </defs>
      <!-- Compass Ring -->
      <circle cx="100" cy="100" r="90" fill="none" stroke="url(#grad1)" stroke-width="12" />
      <!-- Inner Content -->
      <circle cx="100" cy="100" r="75" fill="white" />
      <!-- Needle (Orange) -->
      <path d="M100 30 L125 100 L100 170 L75 100 Z" fill="#F97316" />
      <!-- Person Icon Overlay -->
      <circle cx="100" cy="80" r="15" fill="white" />
      <path d="M85 110 Q100 130 115 110" stroke="white" stroke-width="4" fill="none" />
    </svg>
    """
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}">'

# --- MOCK DATA & UTILS ---
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'employees' not in st.session_state:
        # Mock Employee DB
        st.session_state.employees = pd.DataFrame([
            {"ID": "TP001", "Name": "Sarah Connor", "Role": "VP of People", "Dept": "HR", "Status": "Active", "Performance": 4.8},
            {"ID": "TP002", "Name": "John Smith", "Role": "Senior Engineer", "Dept": "Engineering", "Status": "Active", "Performance": 4.2},
            {"ID": "TP003", "Name": "Emily Chen", "Role": "Product Designer", "Dept": "Product", "Status": "Onboarding", "Performance": 0.0},
            {"ID": "TP004", "Name": "Marcus Johnson", "Role": "Sales Lead", "Dept": "Sales", "Status": "Active", "Performance": 4.5},
        ])
    if 'candidates' not in st.session_state:
        st.session_state.candidates = [
            {"Name": "Alex Rivera", "Role": "Frontend Dev", "Stage": "Interview", "Score": 88},
            {"Name": "Jordan Lee", "Role": "Frontend Dev", "Stage": "Screening", "Score": 75},
        ]

def get_llm_response(messages, api_key, model="openai/gpt-4o-mini"):
    """Centralized AI Handler."""
    if not api_key:
        return "⚠️ API Key missing. Please check settings."
    
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- PDF GENERATOR ---
def create_offer_letter(name, role, salary, start_date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(30, 58, 138) # Brand Blue
    pdf.cell(0, 10, "TalentPilot Inc.", ln=True)
    
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(50, 50, 50)
    pdf.ln(10)
    
    content = f"""
    OFFER OF EMPLOYMENT
    
    Date: {datetime.now().strftime('%B %d, %Y')}
    
    Dear {name},
    
    We are thrilled to offer you the position of {role} at TalentPilot Inc.
    
    COMPENSATION
    Annual Base Salary: ${salary}
    Start Date: {start_date}
    
    BENEFITS
    - Comprehensive Health, Dental, Vision
    - 401(k) Matching
    - Unlimited PTO
    
    We believe your skills will be a valuable asset to our team.
    
    Sincerely,
    
    HR Department
    """
    pdf.multi_cell(0, 8, content)
    return pdf.output(dest='S').encode('latin-1')

# --- MODULES ---

def render_dashboard():
    st.markdown("## 🏠 Executive Dashboard")
    
    # Quick Stats
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
        <div class="tp-card">
            <div class="metric-label">Total Headcount</div>
            <div class="metric-value">142</div>
            <div style="color: #10B981; font-size: 0.8rem;">↑ 12% vs last month</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="tp-card">
            <div class="metric-label">Open Positions</div>
            <div class="metric-value">8</div>
            <div style="color: #F59E0B; font-size: 0.8rem;">3 Urgent</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="tp-card">
            <div class="metric-label">Offer Acceptance</div>
            <div class="metric-value">94%</div>
            <div style="color: #10B981; font-size: 0.8rem;">Top 5% Industry</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="tp-card">
            <div class="metric-label">Avg. Tenure</div>
            <div class="metric-value">2.4y</div>
            <div style="color: #64748b; font-size: 0.8rem;">Stable</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 📈 Recruitment Funnel")
        funnel_data = dict(
            number=[1200, 600, 200, 50, 20],
            stage=["Applied", "Screened", "Interviewed", "Offered", "Hired"]
        )
        fig = px.funnel(funnel_data, x='number', y='stage', color_discrete_sequence=[COLOR_PRIMARY])
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.markdown("### 🌍 Department Distribution")
        dept_counts = st.session_state.employees['Dept'].value_counts().reset_index()
        dept_counts.columns = ['Dept', 'Count']
        fig2 = px.pie(dept_counts, values='Count', names='Dept', hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r)
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)

def render_recruitment(api_key):
    st.markdown("## 👥 Smart Recruitment")
    
    tabs = st.tabs(["Job Description Generator", "Candidate Pipeline", "Resume Parser"])
    
    with tabs[0]:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("### JD Parameters")
            role_title = st.text_input("Job Title", "Senior Python Developer")
            skills = st.text_area("Key Skills", "Python, Streamlit, AWS, AI Agents")
            vibe = st.selectbox("Culture/Vibe", ["Professional", "Startup/Energetic", "Academic"])
            
            if st.button("✨ Generate JD"):
                with st.spinner("AI is drafting..."):
                    prompt = f"Write a {vibe} job description for a {role_title}. Requirements: {skills}. Keep it concise and engaging."
                    jd_text = get_llm_response([{"role": "user", "content": prompt}], api_key)
                    st.session_state.generated_jd = jd_text
        
        with c2:
            if 'generated_jd' in st.session_state:
                st.markdown("### Draft Preview")
                st.markdown(f'<div class="tp-card">{st.session_state.generated_jd}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download .txt", st.session_state.generated_jd, "job_description.txt")

    with tabs[1]:
        st.markdown("### Active Pipeline")
        df = pd.DataFrame(st.session_state.candidates)
        st.dataframe(df, use_container_width=True)

def render_onboarding(api_key):
    st.markdown("## 📋 Onboarding Orchestrator")
    
    st.info("💡 This module uses the Agentic Workflow to connect Offer Generation -> IT Provisioning -> Scheduling.")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("### New Hire Details")
        with st.form("onboard_form"):
            name = st.text_input("Candidate Name")
            role = st.text_input("Role")
            salary = st.text_input("Annual Salary ($)")
            start_date = st.date_input("Start Date")
            submitted = st.form_submit_button("🚀 Launch Onboarding Sequence")
    
    with c2:
        st.markdown("### Workflow Status")
        if submitted and api_key:
            with st.status("Orchestrating...", expanded=True):
                st.write("✅ **Step 1: Offer Letter**")
                pdf_bytes = create_offer_letter(name, role, salary, str(start_date))
                st.download_button("📄 Download Offer PDF", pdf_bytes, f"Offer_{name}.pdf", "application/pdf")
                time.sleep(1)
                
                st.write("✅ **Step 2: IT Provisioning**")
                device = "MacBook Pro" if "Developer" in role else "MacBook Air"
                st.code(f"Provisioning Ticket: REQ-9928\nAsset: {device}\nAccounts: Slack, Jira, G-Suite", language="json")
                time.sleep(1)
                
                st.write("✅ **Step 3: Orientation Schedule**")
                st.caption(f"Calendar invite sent to manager for {start_date}")
                
            st.success(f"Onboarding for {name} initiated successfully!")

def render_employees():
    st.markdown("## 💼 Employee Directory")
    
    search = st.text_input("🔍 Search Employees", placeholder="Name, Role, or ID...")
    
    df = st.session_state.employees
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
        
    st.dataframe(
        df, 
        column_config={
            "Performance": st.column_config.ProgressColumn(
                "Performance Rating",
                help="Last review score",
                format="%.1f",
                min_value=0,
                max_value=5,
            ),
        },
        use_container_width=True
    )
    
    with st.expander("➕ Add New Employee Manually"):
        st.text_input("Name")
        st.text_input("Role")
        st.button("Save to Database")

def render_chat_copilot(api_key):
    """Floating-style Sidebar Chat."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 TalentPilot Assistant")
    
    # Initialize chat history for sidebar
    if "copilot_history" not in st.session_state:
        st.session_state.copilot_history = []

    # Display minimal history (last 3 messages) to save space
    for msg in st.session_state.copilot_history[-3:]:
        bg = "#e0f2fe" if msg["role"] == "user" else "#f1f5f9"
        st.sidebar.markdown(f"""
        <div style="background:{bg}; padding:8px; border-radius:8px; margin-bottom:5px; font-size:0.85rem;">
            <strong>{'You' if msg['role'] == 'user' else 'Pilot'}:</strong> {msg['content']}
        </div>
        """, unsafe_allow_html=True)

    prompt = st.sidebar.text_input("Ask me anything...", key="sidebar_chat")
    if st.sidebar.button("Send", key="sidebar_send") and prompt:
        st.session_state.copilot_history.append({"role": "user", "content": prompt})
        
        with st.sidebar.spinner("Thinking..."):
            # Context-aware system prompt
            sys_prompt = "You are TalentPilot, an HR AI assistant. You help with quick HR lookups, policy questions, and drafting emails."
            messages = [{"role": "system", "content": sys_prompt}] + st.session_state.copilot_history
            
            response = get_llm_response(messages, api_key)
            st.session_state.copilot_history.append({"role": "assistant", "content": response})
            st.rerun()

# --- MAIN APP ---
def main():
    init_session_state()
    
    # -- AUTH SCREEN --
    if not st.session_state.authenticated:
        st.markdown(f"""
            <div class="login-container">
                {get_logo_svg(150)}
                <h1 style="color: {COLOR_PRIMARY}; margin-top: 1rem;">TalentPilot</h1>
                <p style="color: #64748b;">AI-Powered HR Orchestration System</p>
                <div style="margin-top: 2rem;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            api_key = st.text_input("OpenRouter API Key", type="password", help="Required for AI features")
            if st.button("Login to Workspace", use_container_width=True):
                if api_key: # Simple check
                    st.session_state.authenticated = True
                    st.session_state.api_key = api_key
                    st.rerun()
                else:
                    st.error("Please enter an API key (or any string for demo)")
        return

    # -- LOGGED IN UI --
    
    # Sidebar Nav
    with st.sidebar:
        st.markdown(get_logo_svg(80), unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:{COLOR_PRIMARY}'>TalentPilot</h2>", unsafe_allow_html=True)
        
        menu = st.radio("Navigation", [
            "Dashboard", 
            "Recruitment", 
            "Onboarding", 
            "Employee Mgmt", 
            "Performance", 
            "Analytics",
            "Settings"
        ], label_visibility="collapsed")
        
        render_chat_copilot(st.session_state.get('api_key'))

    # Header
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"# {menu}")
        st.markdown(f"Welcome back, **Admin**. Today is {datetime.now().strftime('%A, %B %d')}.")
    with c2:
        st.markdown(" ")
        if st.button("Log Out"):
            st.session_state.authenticated = False
            st.rerun()

    st.markdown("---")

    # Routing
    api_key = st.session_state.get('api_key')
    
    if menu == "Dashboard":
        render_dashboard()
        
    elif menu == "Recruitment":
        render_recruitment(api_key)
        
    elif menu == "Onboarding":
        render_onboarding(api_key)
        
    elif menu == "Employee Mgmt":
        render_employees()
        
    elif menu == "Performance":
        st.markdown("## 📊 Performance Reviews")
        st.info("Select an employee to generate a review template.")
        emp = st.selectbox("Employee", st.session_state.employees['Name'])
        if st.button("Generate Review Template"):
            with st.spinner(f"Drafting 360-review for {emp}..."):
                st.markdown(f"""
                ### 360 Performance Review: {emp}
                **Period:** Q4 2025
                
                **1. Key Achievements**
                * [ ] Met project deadlines
                * [ ] Technical leadership
                
                **2. Areas for Growth**
                * [ ] Public speaking
                * [ ] Documentation
                
                *(Template generated by AI)*
                """)
                
    elif menu == "Analytics":
        st.markdown("## 📈 Deep Analytics")
        # Mock Attrition Data
        dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
        attrition = [2, 1, 3, 0, 1, 2, 4, 1, 2, 1, 0, 1]
        df_att = pd.DataFrame({'Date': dates, 'Exits': attrition})
        
        fig = px.bar(df_att, x='Date', y='Exits', title="Monthly Attrition Trend", color_discrete_sequence=[COLOR_SECONDARY])
        st.plotly_chart(fig, use_container_width=True)
        
    elif menu == "Settings":
        st.markdown("## ⚙️ System Configuration")
        st.toggle("Dark Mode (Beta)")
        st.toggle("Email Notifications")
        st.text_input("Update API Key", type="password", value=api_key)

if __name__ == "__main__":
    main()
