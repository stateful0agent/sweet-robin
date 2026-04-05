import os
import sys
import time
from functions.browser_use import browser_subagent


def login_and_buy_namesilo(domain):
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
    
    3. Once logged in:
       - Search for the domain '{domain}'.
       - Add it to the cart and proceed to checkout.
       - Use the stored card or enter the card details:
         Card Number: {os.environ.get("PREPAID_CARD_NUMBER")}
         Expiry: {os.environ.get("PREPAID_CARD_EXPIRY")}
         CVV: {os.environ.get("PREPAID_CARD_CVV")}
         Name: Robin Agent
         ZIP: {os.environ.get("PREPAID_CARD_ZIP", "94103")}
       - Complete the purchase.
    
    4. Verify if the purchase was successful.
    5. Tell me 'PURCHASE SUCCESSFUL' or describe the error.
    """

    print(f"Attempting to login to NameSilo and buy {domain}...")
    result = browser_subagent(task, url="https://www.namesilo.com/login")
    return result


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "autonomousrobin.news"
    res = login_and_buy_namesilo(domain)
    if res:
        print(f"Result: {res.get('output', 'No output')}")
    else:
        print("No result from browser agent or task failed.")
