# File: agent.py
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from tools import (
    generate_secure_password, 
    invite_user_to_repo, 
    add_user_to_channel, 
    create_onboarding_ticket,
    send_credential_email
)

class AgentState(TypedDict):
    details: dict
    generated_password: str
    logs: List[str]
    error_occurred: bool # <-- NEW: Tracks if we crashed

# --- NODES ---

def step_security(state: AgentState):
    print("... 🔐 Generating Security Credentials ...")
    pw = generate_secure_password()
    state['generated_password'] = pw
    state['logs'].append(f"🔑 Security: Generated temp password.")
    return state

def step_github(state: AgentState):
    print("... 🐙 Managing GitHub Access ...")
    username = state['details'].get('github_username')
    # Logic: Backend Role -> Backend Repo
    repo = "backend-repo" if "backend" in state['details'].get('role', '').lower() else "general-repo"
    
    result = invite_user_to_repo(username, repo)
    state['logs'].append(result['msg'])
    
    # CRITICAL: If this fails, we flag it so we can stop.
    if result['status'] == "error":
        state['error_occurred'] = True
        
    return state

def step_slack(state: AgentState):
    print("... 💬 Managing Slack ...")
    email = state['details'].get('candidate_email')
    channel = "backend-dev"
    result = add_user_to_channel(email, channel)
    state['logs'].append(result['msg'])
    return state

def step_jira(state: AgentState):
    print("... 🎫 Creating Jira Ticket ...")
    email = state['details'].get('candidate_email')
    result = create_onboarding_ticket(email, "Read Documentation")
    state['logs'].append(result['msg'])
    return state

def step_email(state: AgentState):
    print("... 📧 Sending Credentials ...")
    email = state['details'].get('candidate_email')
    pw = state['generated_password']
    result = send_credential_email(email, pw)
    state['logs'].append(result['msg'])
    return state

def step_alert_manager(state: AgentState):
    print("... 🚨 PROCESS FAILED ...")
    state['logs'].append("🛑 STOP: Workflow halted due to previous error. Manager alerted.")
    return state

# --- CONDITIONAL LOGIC ---
# This function decides: Do we continue? or Crash?
def check_health(state: AgentState):
    if state.get('error_occurred'):
        return "failed"
    return "healthy"

# --- BUILD GRAPH ---
workflow = StateGraph(AgentState)

workflow.add_node("security", step_security)
workflow.add_node("github", step_github)
workflow.add_node("slack", step_slack)
workflow.add_node("jira", step_jira)
workflow.add_node("email", step_email)
workflow.add_node("alert_manager", step_alert_manager)

# The Sequence
workflow.set_entry_point("security")
workflow.add_edge("security", "github")

# The Critical Decision Point:
workflow.add_conditional_edges(
    "github",
    check_health,
    {
        "healthy": "slack",        # If GitHub works, go to Slack
        "failed": "alert_manager"  # If GitHub fails, Alert Manager and STOP
    }
)

workflow.add_edge("slack", "jira")
workflow.add_edge("jira", "email")
workflow.add_edge("email", END)
workflow.add_edge("alert_manager", END)

app = workflow.compile()