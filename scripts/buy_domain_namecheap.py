import os
import sys
from functions.browser_use import browser_subagent


def main():
    # Load .env manually
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    os.environ[key] = val

    domain = "autonomousrobin.news"
    username = "sweetrobin163"
    password = os.environ.get("NAMECHEAP_PASSWORD")
    card_number = os.environ.get("PREPAID_CARD_NUMBER")
    card_cvv = os.environ.get("PREPAID_CARD_CVV")
    card_expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    zip_code = "94103"

    if not all([password, card_number, card_cvv, card_expiry]):
        print("Missing Namecheap password or card details in .env")
        return

    task = f"""
    Go to Namecheap (https://www.namecheap.com/myaccount/login/).
    
    1. Log in with username '{username}' and password '{password}'. 
       If you are already logged in, skip this.
    
    2. If it asks for a 2FA code:
       - DO NOT use javascript `fetch()` to call the AgentMail API as it will be blocked by CORS.
       - INSTEAD, open a new tab and navigate to https://agentmail.to/
       - Login with sweet.robin.163@agentmail.to and password {os.environ.get("AGENTMAIL_PASSWORD")}
       - Find the email from Namecheap with the subject "Your confirmation code".
       - The code is likely 'de96ed' (I saw it in a previous attempt), but verify if there is a newer one.
       - Go back to the Namecheap tab and enter the code.

    3. Once logged in, search for 'autonomousrobin.news'.
    4. Add it to the cart.
    5. Proceed to checkout.
    6. Use the prepaid card: {card_number}, CVV: {card_cvv}, Expiry: {card_expiry}, ZIP: 94103.
    7. Complete purchase.
    """

    print(f"Attempting to buy {domain} on Namecheap...")
    result = browser_subagent(task, url="https://www.namecheap.com/myaccount/login/")
    print(f"Status: {result.get('status')}")
    print("Result:", result.get("output"))


if __name__ == "__main__":
    main()
