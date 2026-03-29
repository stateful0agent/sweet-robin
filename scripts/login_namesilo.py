import os
import sys
import time
from functions.browser_use import browser_subagent


def login_namesilo():
    email = "sweet.robin.163@agentmail.to"
    password = os.environ.get("NAMESILO_PASSWORD")
    agentmail_pass = os.environ.get("AGENTMAIL_PASSWORD")

    if not password or not agentmail_pass:
        print("Missing NAMESILO_PASSWORD or AGENTMAIL_PASSWORD in .env")
        return None

    task = f"""
    1. Go to NameSilo.com and login.
       Email: {email}
       Password: {password}
    
    2. If it asks for a device authorization code:
       - Open a new tab and go to https://agentmail.to/
       - Login to AgentMail:
         Address: {email}
         Password: {agentmail_pass}
       - Find the most recent email from NameSilo (support@namesilo.com).
       - Extract the 6-digit code.
       - Go back to the NameSilo tab and enter the code.
       - Submit.
    
    3. Verify if login was successful (e.g., you see a dashboard or "Logout" link).
    4. Tell me 'LOGIN SUCCESSFUL' or describe the error.
    """

    print("Attempting to login to NameSilo...")
    result = browser_subagent(task, url="https://www.namesilo.com/login")
    return result


if __name__ == "__main__":
    res = login_namesilo()
    if res:
        print(f"Result: {res.get('output', 'No output')}")
    else:
        print("No result from browser agent or task failed.")
