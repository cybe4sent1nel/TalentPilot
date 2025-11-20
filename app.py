import streamlit as st
import json
import datetime
from fpdf import FPDF
from openai import OpenAI
import time
import base64

# --- CONFIGURATION & STYLE ---
st.set_page_config(
    page_title="TalentPilot | AI HR Workspace",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ASSETS & LOGO GENERATION ---
def get_logo_svg():
    """Generates a Green/White SVG Logo for TalentPilot."""
    # A modern abstract 'T' / Leaf shape in Green 60
    svg = """
    <svg width="150" height="150" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <circle cx="100" cy="100" r="90" fill="#198038" />
      <path d="M100 40 L100 160 M60 60 L140 60" stroke="white" stroke-width="20" stroke-linecap="round" />
      <path d="M100 100 L140 60" stroke="white" stroke-width="15" stroke-linecap="round" />
    </svg>
    """
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="80" style="margin-bottom: 1rem;">'

# --- CUSTOM CSS (GREEN THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff;
        color: #161616;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f4f4f4;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Header Styling */
    .header-container {
        padding: 2rem;
        background: linear-gradient(135deg, #198038 0%, #0E6027 100%); /* IBM Green 60 to 70 */
        color: white;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Primary Button - Green 60 */
    .stButton>button {
        background-color: #198038;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #0E6027; /* Green 70 */
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Login Box */
    .auth-box {
        max-width: 400px;
        margin: 6rem auto;
        background: white;
        padding: 2.5rem;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    /* Chat Bubbles */
    .chat-user {
        background-color: #E8F5E9; /* Light Green */
        color: #0E6027;
        padding: 1rem;
        border-radius: 12px 12px 0 12px;
        margin-bottom: 10px;
        text-align: right;
        border: 1px solid #C8E6C9;
    }
    .chat-bot {
        background-color: white;
        border: 1px solid #e0e0e0;
        color: #161616;
        padding: 1.5rem;
        border-radius: 12px 12px 12px 0;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    /* Status Indicators */
    .status-box {
        padding: 1rem;
        border-left: 4px solid #198038;
        background: #f9f9f9;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION SYSTEM ---
def check_auth():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown(f"""
            <div class="auth-box">
                {get_logo_svg()}
                <h2 style="color: #198038; margin-top:0;">TalentPilot</h2>
                <p style="color: #525252; font-size: 0.9rem;">Secure Agentic HR Workspace</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            username = st.text_input("Username", placeholder="admin", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="admin", label_visibility="collapsed")
            
            if st.button("Log In to Workspace", use_container_width=True):
                if username == "admin" and password == "admin":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Access Denied.")
        return False
    return True

# --- REAL SKILLS (TOOLS) ---

def generate_offer_letter(candidate_name, role, salary, start_date):
    """Generates a professional, multi-page PDF offer letter."""
    pdf = FPDF()
    pdf.add_page()
    
    # -- Page 1: Formal Offer --
    # Letterhead
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(25, 128, 56) # Green 60
    pdf.cell(0, 10, "TalentPilot", ln=True, align='L')
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "123 Innovation Drive, Tech City, NY", ln=True)
    pdf.ln(10)
    
    # Title
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "OFFER OF EMPLOYMENT", ln=True, align='C')
    pdf.ln(5)
    
    # Body Text
    pdf.set_font("Arial", '', 11)
    current_date = datetime.date.today().strftime("%B %d, %Y")
    
    body = f"""
    {current_date}

    Dear {candidate_name},

    We are pleased to extend an offer of employment for the position of {role} at TalentPilot Inc. We were impressed with your skills and experience, and we believe you will be a fantastic addition to our team.

    1. Position & Start Date
    Your position will be {role}, reporting to the Head of Department. Your anticipated start date is {start_date}.

    2. Compensation
    Your starting annual base salary will be ${salary}, paid on a semi-monthly basis. In addition, you will be eligible for our annual performance bonus plan with a target of 15% of your base salary.

    3. Benefits
    You will be eligible to participate in the Company's comprehensive benefits program, which includes:
      - Medical, Dental, and Vision Insurance (100% premiums covered)
      - 401(k) Retirement Plan with 5% matching
      - Unlimited Paid Time Off (PTO) policy
      - $2,000 Annual Learning Stipend

    4. Stock Options
    Subject to approval by the Board of Directors, you will be granted an option to purchase 5,000 shares of the Company's Common Stock.

    5. At-Will Employment
    Your employment with the Company is "at-will." This means that either you or the Company may terminate the employment relationship at any time, with or without cause or notice.

    We look forward to you joining us!

    Sincerely,

    Sarah Connor
    VP of People, TalentPilot
    """
    pdf.multi_cell(0, 6, body)
    pdf.ln(15)
    
    # Signature Line
    pdf.cell(0, 10, "__________________________", ln=True)
    pdf.cell(0, 5, "Candidate Signature", ln=True)
    
    # Output
    filename = f"Offer_Letter_{candidate_name.replace(' ', '_')}.pdf"
    return filename, pdf.output(dest='S').encode('latin-1')

def provision_it_hardware(candidate_name, role):
    """Simulates calling ServiceNow API."""
    is_eng = any(x in role.lower() for x in ["engineer", "developer", "data", "architect"])
    device = "MacBook Pro 16\" M3 Max" if is_eng else "MacBook Air 15\" M3"
    ticket_id = f"REQ-{int(time.time())}-77"
    
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "assigned_device": device,
        "accessories": ["Magic Keyboard", "Magic Mouse", "4K Monitor"] if is_eng else ["Magic Mouse"],
        "software_bundle": "Engineering_Suite_V2" if is_eng else "General_Business_Suite"
    }

def schedule_welcome_lunch(candidate_name, team_name, date):
    """Simulates Google Calendar API."""
    return {
        "status": "confirmed",
        "event_link": "https://calendar.google.com/event?eid=xyz",
        "attendees": [f"manager@{team_name}.com", "team@talentpilot.ai"],
        "time": f"{date} at 12:30 PM EST",
        "location": "The Green Room (Cafeteria)"
    }

# --- ORCHESTRATION ENGINE ---
def get_llm_response(messages, api_key):
    """Connects to OpenRouter/watsonx."""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_offer_letter",
                "description": "Create a detailed PDF offer letter contract.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_name": {"type": "string"},
                        "role": {"type": "string"},
                        "salary": {"type": "string"},
                        "start_date": {"type": "string", "description": "YYYY-MM-DD"}
                    },
                    "required": ["candidate_name", "role", "salary", "start_date"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "provision_it_hardware",
                "description": "Order laptop and equipment via ServiceNow.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_name": {"type": "string"},
                        "role": {"type": "string"}
                    },
                    "required": ["candidate_name", "role"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "schedule_welcome_lunch",
                "description": "Book a team lunch on the calendar.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_name": {"type": "string"},
                        "team_name": {"type": "string"},
                        "date": {"type": "string"}
                    },
                    "required": ["candidate_name", "team_name", "date"]
                }
            }
        }
    ]

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto", 
        )
        return response.choices[0].message
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# --- MAIN APP LOGIC ---

def main():
    if not check_auth():
        return

    # Sidebar
    with st.sidebar:
        st.markdown(get_logo_svg(), unsafe_allow_html=True)
        st.markdown("### **TalentPilot**")
        st.caption("Agentic HR Workspace v2.0")
        st.markdown("---")
        
        api_key = st.text_input("Agent API Key", type="password")
        
        st.markdown("#### ⚡ Connected Systems")
        st.success("🟢 DocuSign (Contracts)")
        st.success("🟢 ServiceNow (Hardware)")
        st.success("🟢 Workday (HRIS)")
        st.success("🟢 G-Suite (Calendar)")
        
        if st.button("Clear Context"):
            st.session_state.messages = []
            st.rerun()

    # Main Banner
    # Using a professional office stock image for the banner
    st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2301&auto=format&fit=crop", 
             use_container_width=True, caption="TalentPilot Operations Center")

    st.title("Good Morning, HR Team.")
    st.markdown("Your AI agent is ready to assist with onboarding, procurement, and scheduling.")

    if not api_key:
        st.info("Please enter your API Key in the sidebar to activate the neural engine.")
        st.stop()

    # Initialize History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are TalentPilot, an expert HR AI. You are professional, efficient, and helpful. You coordinate onboarding by calling relevant tools."}
        ]

    # Display Chat
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            # Render Tool Usage
            if msg.get("tool_calls"):
                with st.status("🧠 Thinking & Orchestrating...", expanded=False):
                    for tool in msg["tool_calls"]:
                        fn = tool['function']['name']
                        args = json.loads(tool['function']['arguments'])
                        st.markdown(f"**Activating Skill:** `{fn}`")
                        st.code(json.dumps(args, indent=2), language='json')
            
            # Render Content
            content = msg.get("content")
            if content:
                with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🌱"):
                    st.write(content)

    # User Input
    if prompt := st.chat_input("Try: 'Onboard Alex Chen as Senior Engineer, $160k salary, starting Dec 1st'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)

        # AI Response
        with st.chat_message("assistant", avatar="🌱"):
            with st.spinner("Processing Request..."):
                response = get_llm_response(st.session_state.messages, api_key)
                
                if response:
                    msg_data = response.model_dump()
                    
                    # Tool Handling
                    if msg_data.get("tool_calls"):
                        st.session_state.messages.append(msg_data)
                        
                        for tool_call in msg_data["tool_calls"]:
                            fn_name = tool_call['function']['name']
                            args = json.loads(tool_call['function']['arguments'])
                            
                            # UI for Action
                            with st.container():
                                st.markdown(f"### ⚡ Action: {fn_name.replace('_', ' ').title()}")
                                
                                if fn_name == "generate_offer_letter":
                                    fname, pdf_bytes = generate_offer_letter(**args)
                                    st.success("Offer Letter Generated Successfully")
                                    st.download_button("📥 Download Signed PDF", pdf_bytes, fname, "application/pdf")
                                    tool_res = f"Generated {fname}"
                                    
                                elif fn_name == "provision_it_hardware":
                                    time.sleep(1)
                                    res = provision_it_hardware(**args)
                                    st.success(f"Hardware Ordered: {res['ticket_id']}")
                                    st.json(res)
                                    tool_res = json.dumps(res)
                                    
                                elif fn_name == "schedule_welcome_lunch":
                                    time.sleep(1)
                                    res = schedule_welcome_lunch(**args)
                                    st.success("Calendar Event Created")
                                    st.info(f"{res['time']} @ {res['location']}")
                                    tool_res = json.dumps(res)
                                    
                                else:
                                    tool_res = "Error: Skill not found"

                                # Save Tool Result
                                st.session_state.messages.append({
                                    "tool_call_id": tool_call['id'],
                                    "role": "tool",
                                    "name": fn_name,
                                    "content": tool_res
                                })
                        
                        # Final Wrap-up
                        final_res = get_llm_response(st.session_state.messages, api_key)
                        if final_res and final_res.content:
                            st.write(final_res.content)
                            st.session_state.messages.append(final_res.model_dump())

                    # Standard Text Response
                    elif msg_data.get("content"):
                        st.write(msg_data["content"])
                        st.session_state.messages.append(msg_data)

if __name__ == "__main__":
    main()
