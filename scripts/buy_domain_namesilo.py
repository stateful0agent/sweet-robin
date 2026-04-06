import sys
import os
from functions.browser_use import browser_subagent


def buy_domain_namesilo(domain):
    # Load .env manually
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    os.environ[key] = val

    email = "sweet.robin.163@agentmail.to"
    password = os.environ.get("NAMESILO_PASSWORD")
    card_num = os.environ.get("PREPAID_CARD_NUMBER")
    expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    cvv = os.environ.get("PREPAID_CARD_CVV")
    name = "Sweet Robin"
    address = "123 Main St, San Francisco, CA 94103"

    if not all([password, card_num, expiry, cvv]):
        print("Missing NameSilo password or card details in .env")
        return None

    task = f"""
    Go to NameSilo.com and search for '{domain}'.
    Add '{domain}' to the cart and proceed to checkout.
    Login with:
    Email: {email}
    Password: {password}
    
    If it asks for a device authorization code:
    - Open a new tab and go to https://agentmail.to/
    - Login to AgentMail:
      Address: {email}
      Password: {os.environ.get("AGENTMAIL_PASSWORD")}
    - Find the most recent email from NameSilo (support@namesilo.com).
    - Extract the 6-digit code.
    - Go back to the NameSilo tab and enter the code.
    - Submit.
    
    In the payment section, select 'Credit Card'.
    Enter:
    Card Number: {card_num}
    Expiry: {expiry}
    CVV: {cvv}
    Billing Name: {name}
    Billing Address: {address}
    
    Attempt to complete the purchase. 
    If successful, report the order ID. 
    If it fails, report the error message displayed on the site.
    """

    result = browser_subagent(task, url="https://www.namesilo.com")
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/buy_domain_namesilo.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    res = buy_domain_namesilo(domain)
    if res:
        print(res.get("output", "No output from browser agent"))
    else:
        print("Failed to start buy task.")
