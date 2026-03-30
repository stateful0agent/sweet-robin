import os
import sys
import time
from functions.browser_use import browser_subagent


def buy_domain_porkbun():
    email = "sweet.robin.163@agentmail.to"
    agentmail_pass = os.environ.get("AGENTMAIL_PASSWORD")
    username = "sweetrobin163"
    password = os.environ.get("PORKBUN_PASSWORD")
    card_num = os.environ.get("PREPAID_CARD_NUMBER")
    expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    if not all([agentmail_pass, password, card_num, expiry, cvv]):
        print("Missing AgentMail password, Porkbun password, or card details in .env")
        return None

    task = f"""
    1. Go to https://porkbun.com/account/login
    2. Login with username '{username}' and password '{password}'.
    3. If it asks for a device verification code:
       - Open a new tab and go to https://agentmail.to/
       - Login to AgentMail (Email: {email}, Password: {agentmail_pass}).
       - Find the most recent email from Porkbun (support@porkbun.com).
       - Extract the 10-character code.
       - Go back to the Porkbun tab and enter the code.
       - Submit.
    4. Once logged in, search for 'autonomousrobin.news'.
    5. Add it to the cart.
    6. Proceed to checkout.
    7. Select 'Credit Card' as payment method.
    8. Enter card details:
       - Card Number: {card_num}
       - Expiry: {expiry}
       - CVV: {cvv}
       - Billing Name: Sweet Robin
       - Billing Address: 123 Main St, San Francisco, CA {card_zip}
    9. Complete the purchase.
    10. Report SUCCESS and the order ID if successful.
    11. If it fails with 3DS or other, tell me the exact error.
    """

    print("Attempting to buy domain on Porkbun with 2FA handling...")
    result = browser_subagent(task, url="https://porkbun.com/account/login")
    return result


if __name__ == "__main__":
    res = buy_domain_porkbun()
    if res:
        print(f"Result: {res.get('status')} | {res.get('output', 'No output')}")
    else:
        print("No result from browser agent or task failed.")
