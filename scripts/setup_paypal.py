import os
import sys
import time
from functions.browser_use import browser_subagent


def setup_paypal():
    email = "sweet.robin.163@agentmail.to"
    agentmail_pass = os.environ.get("AGENTMAIL_PASSWORD")
    card_num = os.environ.get("PREPAID_CARD_NUMBER")
    expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    if not all([agentmail_pass, card_num, expiry, cvv]):
        print("Missing AgentMail password or card details in .env")
        return None

    # New password to set if reset is needed
    new_paypal_pass = "SweetRobin2026!#"

    task = f"""
    1. Go to https://www.paypal.com/signin
    2. Enter {email} and click 'Next'.
    3. If it asks for a password, try '{new_paypal_pass}'.
    4. If that fails (or if it doesn't ask for a password but says something else), click 'Forgot Password?'.
    5. Choose to receive a code via email.
    6. Open a new tab and go to https://agentmail.to/
    7. Login to AgentMail (Email: {email}, Password: {agentmail_pass}).
    8. Find the most recent email from PayPal (service@paypal.com).
    9. Extract the 6-digit code.
    10. Go back to the PayPal tab and enter the code.
    11. Set the new password to '{new_paypal_pass}'.
    12. Once logged in, go to 'Wallet'.
    13. Click 'Link a card'.
    14. Enter card details:
        - Card Number: {card_num}
        - Expiry: {expiry}
        - CVV: {cvv}
        - Billing Address: 123 Main St, San Francisco, CA {card_zip}
    15. If it asks to confirm the card (e.g., small charge), tell me.
    16. Report SUCCESS if the card is linked.
    """

    print("Attempting to setup/reset PayPal and link the card...")
    result = browser_subagent(task, url="https://www.paypal.com/signin")
    return result, new_paypal_pass


if __name__ == "__main__":
    result = setup_paypal()
    if result:
        res, new_pass = result
        print(f"Result: {res.get('status')} | {res.get('output', 'No output')}")
        if "SUCCESS" in res.get("output", "").upper():
            print(f"PayPal setup SUCCESS. Password set to: {new_pass}")
    else:
        print("No result from browser agent or task failed.")
