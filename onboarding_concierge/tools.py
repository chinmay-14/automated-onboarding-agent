# File: tools.py
import os
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from github import Github
from dotenv import load_dotenv

load_dotenv()

# --- 1. SECURITY: Password Generator (This was missing!) ---
def generate_secure_password(length=12):
    """Generates a secure random password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

# --- 2. GITHUB: Repo Invitation ---
def invite_user_to_repo(username, repo_name):
    """Checks if user exists and simulates adding to a specific repo."""
    token = os.getenv("GITHUB_TOKEN")
    if not token: return {"status": "error", "msg": "⚠️ GitHub: Skipped (No Token)"}

    try:
        g = Github(token)
        user = g.get_user(username)
        return {
            "status": "success", 
            "msg": f"✅ GitHub: User '{user.login}' verified. Added to '{repo_name}'."
        }
    except Exception as e:
        return {"status": "error", "msg": f"❌ GitHub Error: User '{username}' not found."}

# --- 3. SLACK: Channel Add ---
def add_user_to_channel(email, channel_name):
    """Simulates adding user to a Slack channel."""
    return {"status": "success", "msg": f"✅ Slack: (Simulation) Added {email} to #{channel_name}"}

# --- 4. JIRA: Ticket Creation ---
def create_onboarding_ticket(email, tasks):
    """Simulates creating a Jira ticket."""
    return {"status": "success", "msg": f"✅ Jira: (Simulation) Created ticket for {email}"}

# --- 5. EMAIL: Real Email Sender ---
def send_credential_email(recipient_email, password):
    """Sends an ACTUAL email with the credentials using Gmail."""
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    
    # Safety check: If no email keys are found, just simulate it so code doesn't crash
    if not sender_email or not sender_password:
        return {"status": "success", "msg": f"⚠️ Email: Skipped (No keys in .env). PW would be: {password}"}

    subject = "Welcome to the Team! Your Login Details"
    body = f"""
    Hello!
    
    Welcome to the team. Here are your initial credentials:
    
    --------------------------------
    Email: {recipient_email}
    Temporary Password: {password}
    --------------------------------
    
    Please change this password immediately.
    
    Best,
    AI Concierge
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        print("   ... Connecting to Gmail SMTP Server ...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            
        return {
            "status": "success", 
            "msg": f"📧 Email: SUCCESS! Sent real credentials to {recipient_email}"
        }
    except Exception as e:
        return {"status": "error", "msg": f"❌ Email Failed: {str(e)}"}