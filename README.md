# ⚡ Automated Onboarding Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/AI-Gemini%202.0-orange)
![Orchestration](https://img.shields.io/badge/Orchestration-LangGraph-green)

**A stateful AI agent that automates the IT provisioning lifecycle for new hires.**

Instead of manual tickets and emails, this agent parses natural language requests (e.g., *"Onboard Alice to the Backend Team"*) and autonomously executes the necessary API calls to set up accounts.



## 🚀 Key Features

* **Semantic Parsing:** Uses **Google Gemini 2.0 Flash** to extract structured data (JSON) from unstructured manager requests.
* **Identity Verification:** Connects to **GitHub API** to verify user existence before attempting invites.
* **Conditional Workflow:** Implements **LangGraph** logic—if GitHub verification fails, the workflow halts immediately to prevent downstream errors.
* **Real-World Actions:** Generates secure temporary credentials and dispatches them via **SMTP (Gmail)**.
* **Interactive UI:** Built with **Streamlit** for a clean, demo-ready interface.

## 🛠️ Architecture

1.  **Input:** Manager types request into Streamlit UI.
2.  **Parsing:** Gemini extracts `candidate_email`, `role`, and `github_username`.
3.  **Validation:** Agent hits GitHub API to validate the username.
4.  **Routing:**
    * ✅ **Success:** Proceed to generate password -> Mock Slack invite -> Mock Jira ticket -> Send Email.
    * ❌ **Failure:** Trigger `failure_handler` node and stop execution.

## 📦 Setup & Usage

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/automated-onboarding-agent.git](https://github.com/YOUR_USERNAME/automated-onboarding-agent.git)
    cd automated-onboarding-agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file:
    ```ini
    GEMINI_API_KEY=your_key
    GITHUB_TOKEN=your_pat
    EMAIL_SENDER=your_gmail
    EMAIL_PASSWORD=your_app_password
    ```

4.  **Run the App:**
    ```bash
    streamlit run ui.py
    ```

## 📝 Project Status
* **GitHub Integration:** Live (Read/Write)
* **Email Integration:** Live (SMTP)
* **Slack/Jira:** Simulation Mode (Pending Enterprise Keys)
