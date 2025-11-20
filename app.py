import streamlit as st
import json
import datetime
from fpdf import FPDF
from openai import OpenAI
import time

# --- CONFIGURATION & STYLE ---
st.set_page_config(
    page_title="HR Orchestrate Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a Professional IBM-like Look
st.markdown("""
    <style>
    .main {
        background-color: #f4f7f6;
    }
    .stButton>button {
        background-color: #0f62fe;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #0353e9;
    }
    .auth-container {
        background-color: white;
        padding: 3rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: auto;
    }
    .success-msg {
        padding: 1rem;
        background-color: #defbe6;
        border: 1px solid #24a148;
        color: #1e8439;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION SYSTEM ---
def check_auth():
    """Simple session-based authentication simulation."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("## 🔐 HR Portal Login")
            st.markdown("Please sign in to access the Agentic Workflow.")
            
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="admin")
            
            if st.button("Sign In"):
                if username == "admin" and password == "admin":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. (Try admin/admin)")
        return False
    return True

# --- REAL SKILLS (TOOLS) ---
# In watsonx Orchestrate, these would be OpenAPI skills imported from Swagger files.

def generate_offer_letter(candidate_name, role, salary, start_date):
    """Generates a physical PDF offer letter."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ACME Corp - Official Offer", ln=1, align='C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Arial", size=12)
    content = f"""
    Date: {datetime.date.today()}
    
    Dear {candidate_name},
    
    We are pleased to offer you the position of {role} at ACME Corp.
    
    Key Details:
    - Starting Salary: ${salary}
    - Start Date: {start_date}
    - Location: Hybrid / New York
    
    We are impressed by your background and look forward to welcoming you 
    to the team.
    
    Sincerely,
    
    The HR Team
    """
    pdf.multi_cell(0, 10, content)
    
    # Output
    filename = f"offer_{candidate_name.replace(' ', '_')}.pdf"
    # Saving to a temporary path (simulation of cloud storage)
    # In a real app, we might upload this to S3/Box
    return filename, pdf.output(dest='S').encode('latin-1')

def provision_it_hardware(candidate_name, role):
    """Simulates calling ServiceNow to provision hardware."""
    # Logic: Engineers get Macs, others get ThinkPads
    device = "MacBook Pro M3" if "engineer" in role.lower() or "developer" in role.lower() else "Lenovo ThinkPad X1"
    ticket_id = f"INC-{int(time.time())}"
    
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "assigned_device": device,
        "software_bundle": ["Slack", "Office365", "Zoom", "VS Code" if "engineer" in role.lower() else "Excel"]
    }

def schedule_welcome_lunch(candidate_name, team_name, date):
    """Simulates an Outlook/Google Calendar Integration."""
    return {
        "status": "scheduled",
        "event": f"Welcome Lunch for {candidate_name}",
        "attendees": [f"manager@{team_name}.com", "hr@acme.com"],
        "time": f"{date} at 12:00 PM",
        "location": "Main Cafeteria"
    }

# --- ORCHESTRATION ENGINE ---
def get_llm_response(messages, api_key):
    """Interacts with OpenRouter (acting as watsonx.ai)"""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    # Define tools for the LLM (Function Calling)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_offer_letter",
                "description": "Create and download a PDF offer letter for a new hire.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_name": {"type": "string"},
                        "role": {"type": "string"},
                        "salary": {"type": "string"},
                        "start_date": {"type": "string", "description": "YYYY-MM-DD format"}
                    },
                    "required": ["candidate_name", "role", "salary", "start_date"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "provision_it_hardware",
                "description": "Trigger IT provisioning for a laptop and software.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "candidate_name": {"type": "string"},
                        "role": {"type": "string", "description": "Job title to determine hardware specs"}
                    },
                    "required": ["candidate_name", "role"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "schedule_welcome_lunch",
                "description": "Schedule a calendar invite for the team lunch.",
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
            model="openai/gpt-4o-mini", # Or any robust model on OpenRouter
            messages=messages,
            tools=tools,
            tool_choice="auto", 
        )
        return response.choices[0].message
    except Exception as e:
        st.error(f"LLM Error: {e}")
        return None

# --- MAIN APP LOGIC ---

def main():
    if not check_auth():
        return

    # Sidebar Config
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg", width=100)
        st.markdown("### ⚙️ Configuration")
        api_key = st.text_input("OpenRouter API Key", type="password", help="Required for the Orchestration Engine")
        
        st.markdown("---")
        st.markdown("### 🧠 Active Skills")
        st.info("✅ DocuGen (PDF)")
        st.info("✅ ServiceNow (IT)")
        st.info("✅ Outlook (Calendar)")
        
        st.markdown("---")
        if st.button("Clear Session"):
            st.session_state.messages = []
            st.rerun()

    # Main Interface
    st.title("🤖 HR Orchestration Agent")
    st.markdown("*Powered by watsonx Orchestrate (Simulation)*")
    
    # Warning if no key
    if not api_key:
        st.warning("⚠️ Please enter your OpenRouter API Key in the sidebar to activate the agent.")
        st.stop()

    # Chat History Initialization
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are an advanced HR Orchestration Agent. You help HR managers onboard employees by autonomously calling tools to generate offers, provision IT assets, and schedule meetings. Always confirm actions before finalizing."}
        ]

    # Display Chat
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                content = msg.get("content")
                # Check if there was a tool call (visualize it)
                if msg.get("tool_calls"):
                    with st.status("🤖 Orchestrating Skills...", expanded=False):
                        for tool in msg["tool_calls"]:
                            st.write(f"**Skill Triggered:** `{tool.function.name}`")
                            st.json(tool.function.arguments)
                if content:
                    st.write(content)

    # Input Area
    if prompt := st.chat_input("E.g., Onboard Alice Smith as a Senior Engineer starting Nov 25th..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get LLM Response
        with st.chat_message("assistant"):
            with st.spinner("Reasoning..."):
                response_message = get_llm_response(st.session_state.messages, api_key)

                # HANDLER FOR TOOL CALLS
                if response_message and response_message.tool_calls:
                    # 1. Add the assistant's "thought" (tool call request) to history
                    st.session_state.messages.append(response_message)
                    
                    # 2. Execute Tools
                    for tool_call in response_message.tool_calls:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)
                        
                        tool_result = None
                        
                        # UI Feedback
                        with st.status(f"⚙️ Executing: {function_name}", expanded=True) as status:
                            
                            if function_name == "generate_offer_letter":
                                fname, pdf_data = generate_offer_letter(**arguments)
                                tool_result = f"Offer letter generated: {fname}"
                                # Create download button immediately
                                st.download_button(
                                    label="📄 Download Generated Offer PDF",
                                    data=pdf_data,
                                    file_name=fname,
                                    mime="application/pdf"
                                )
                                status.update(label="✅ PDF Generated!", state="complete")
                                
                            elif function_name == "provision_it_hardware":
                                time.sleep(1) # Simulate API latency
                                res = provision_it_hardware(**arguments)
                                tool_result = json.dumps(res)
                                st.success(f"IT Ticket Created: {res['ticket_id']}")
                                st.info(f"Provisioning: {res['assigned_device']}")
                                status.update(label="✅ IT Request Sent!", state="complete")
                                
                            elif function_name == "schedule_welcome_lunch":
                                time.sleep(1)
                                res = schedule_welcome_lunch(**arguments)
                                tool_result = json.dumps(res)
                                st.success(f"Calendar Event: {res['event']} @ {res['time']}")
                                status.update(label="✅ Calendar Updated!", state="complete")

                            else:
                                tool_result = "Error: Unknown function"

                        # 3. Append Tool Result to History
                        st.session_state.messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": tool_result,
                            }
                        )

                    # 4. Get Final Follow-up Response from LLM (Reading the tool outputs)
                    final_response = get_llm_response(st.session_state.messages, api_key)
                    if final_response and final_response.content:
                        st.write(final_response.content)
                        st.session_state.messages.append({"role": "assistant", "content": final_response.content})

                # HANDLER FOR NORMAL CONVERSATION
                elif response_message and response_message.content:
                    st.write(response_message.content)
                    st.session_state.messages.append({"role": "assistant", "content": response_message.content})

if __name__ == "__main__":
    main()
