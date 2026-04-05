import os
import sys
import time
from functions.browser_use import browser_subagent


def login_namesilo(code):
    email = "sweet.robin.163@agentmail.to"
    password = os.environ.get("NAMESILO_PASSWORD")

    if not password:
        print("Missing NAMESILO_PASSWORD in .env")
        return None

    task = f"""
    1. Go to https://www.namesilo.com/login and login.
       Email: {email}
       Password: {password}
    
    2. If it asks for a device authorization code:
       - Use this code: {code}
       - Submit.
    
    3. Once logged in:
       - Go to the 'Basket' or 'Cart'.
       - Proceed to checkout.
       - Use the stored card or enter the card details:
         Card Number: {os.environ.get("PREPAID_CARD_NUMBER")}
         Expiry: {os.environ.get("PREPAID_CARD_EXPIRY")}
         CVV: {os.environ.get("PREPAID_CARD_CVV")}
         Name: Robin Agent
         ZIP: {os.environ.get("PREPAID_CARD_ZIP", "94103")}
       - Complete the purchase for 'autonomousrobin.news'.
    
    4. Verify if the purchase was successful.
    5. Tell me 'PURCHASE SUCCESSFUL' or describe the error.
    """

    print(f"Attempting to login to NameSilo with code {code} and complete purchase...")
    result = browser_subagent(task, url="https://www.namesilo.com/login")
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/login_namesilo_with_code.py <code>")
        sys.exit(1)

    code = sys.argv[1]
    res = login_namesilo(code)
    if res:
        print(f"Result: {res.get('output', 'No output')}")
    else:
        print("No result from browser agent or task failed.")
