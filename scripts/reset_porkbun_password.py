import os
import sys
import time
from functions.browser_use import browser_subagent


def reset_porkbun():
    email = "sweet.robin.163@agentmail.to"
    agentmail_pass = os.environ.get("AGENTMAIL_PASSWORD")
    username = "sweetrobin163"

    if not all([agentmail_pass]):
        print("Missing AgentMail password in .env")
        return None

    # New password to set if reset is needed
    new_porkbun_pass = "RobinStrongPork2026!#"

    task = f"""
    1. Go to https://porkbun.com/account/login
    2. Click 'Forgot password?'.
    3. Enter username '{username}' and submit.
    4. If it asks for an email instead, enter '{email}'.
    5. Choose to receive a code via email.
    6. Open a new tab and go to https://agentmail.to/
    7. Login to AgentMail (Email: {email}, Password: {agentmail_pass}).
    8. Find the most recent email from Porkbun (support@porkbun.com).
    9. Extract the 6-digit code or follow the link.
    10. Go back to the Porkbun tab and enter the code or use the link.
    11. Set the new password to '{new_porkbun_pass}'.
    12. Verify that login is successful.
    13. Tell me 'RESET SUCCESSFUL' or describe the error.
    """

    print("Attempting to reset Porkbun password...")
    result = browser_subagent(task, url="https://porkbun.com/account/login")
    return result, new_porkbun_pass


if __name__ == "__main__":
    result = reset_porkbun()
    if result:
        res, new_pass = result
        print(f"Result: {res.get('status')} | {res.get('output', 'No output')}")
        if "SUCCESS" in res.get("output", "").upper():
            print(f"Porkbun reset SUCCESS. New Password: {new_pass}")
    else:
        print("No result from browser agent or task failed.")
