# File: ui.py
import streamlit as st
import json
from parser import parse_user_request
from agent import app

# 1. Configure the Page
st.set_page_config(page_title="AI Concierge", page_icon="🤖")
st.title("🤖 AI Onboarding Agent")
st.markdown("---")

# 2. Input Section
st.subheader("Who are we hiring today?")
user_input = st.text_area(
    "Enter instructions:", 
    height=100,
    placeholder="Example: Onboard Alice (alice@test.com) to the Backend Team. GitHub: chinmay-14"
)

# 3. The "Go" Button
if st.button("🚀 Start Onboarding Process"):
    
    if not user_input:
        st.warning("Please enter some text first.")
    else:
        # --- PHASE 1: PARSING (The Brain) ---
        with st.spinner("🧠 Gemini is thinking..."):
            try:
                json_str = parse_user_request(user_input)
                data = json.loads(json_str)
                
                # Show the user what Gemini found (in a nice JSON box)
                st.success("✅ Request Understood!")
                st.json(data)
                
            except Exception as e:
                st.error(f"Parsing Error: {e}")
                st.stop()

        # --- PHASE 2: EXECUTION (The Hands) ---
        st.subheader("⚙️ Workflow Execution")
        progress_bar = st.progress(0)
        
        # Prepare the agent
        initial_state = {
            "details": data, 
            "generated_password": "", 
            "logs": [], 
            "error_occurred": False
        }

        with st.spinner("🤖 Agent is working... (Checking GitHub, sending Emails)"):
            result = app.invoke(initial_state)
            progress_bar.progress(100)

        # --- PHASE 3: RESULTS ---
        st.subheader("📜 Final Report")
        
        for log in result['logs']:
            if "✅" in log:
                st.success(log)
            elif "❌" in log:
                st.error(log)
            elif "🛑" in log:
                st.error(log)
            else:
                st.info(log)
                
        if not result.get('error_occurred'):
            st.balloons() # Fun animation on success!