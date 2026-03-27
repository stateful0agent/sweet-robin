import os
import sys
import secrets
import string
from functions.browser_use import browser_subagent


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for i in range(length))


def main():
    vps_pass = os.environ.get("RACKNERD_VPS_PASSWORD")
    if not vps_pass:
        vps_pass = generate_password()
        # Save it to .env
        os.system(f"uv run scripts/set_secret.py RACKNERD_VPS_PASSWORD '{vps_pass}'")

    rn_pass = os.environ.get("RACKNERD_ACCOUNT_PASSWORD")
    if not rn_pass:
        rn_pass = generate_password()
        # Save it to .env
        os.system(f"uv run scripts/set_secret.py RACKNERD_ACCOUNT_PASSWORD '{rn_pass}'")

    card_number = os.environ.get("PREPAID_CARD_NUMBER")
    card_expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    card_cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP")
    email = os.environ.get("AGENTMAIL_ADDRESS")

    task = f"""
1. Go to https://www.racknerd.com/specials
2. Find a VPS plan under $20/year (e.g., 1GB RAM for $10.60/year or 2GB RAM for $18.66/year).
3. Click 'Order' on the chosen plan.
4. On the configuration page:
   - Hostname: autonomousrobin
   - Root Password: {vps_pass}
   - OS: Ubuntu 24.04 (prefer newest LTS available)
   - Location: Los Angeles or Seattle (prefer US West)
5. Continue to the next step.
6. In the shopping cart, click 'Checkout'.
7. In the Checkout page (Create New Account):
   - First Name: Sweet
   - Last Name: Robin
   - Email: {email}
   - Company: Autonomous Robin
   - Address 1: 101 California St
   - City: San Francisco
   - State: CA
   - Postcode: {card_zip}
   - Country: United States
   - Password: {rn_pass}
8. Payment Method: Credit Card (Stripe) or Credit Card.
9. Card Details:
   - Number: {card_number}
   - Expiry: {card_expiry}
   - CVV: {card_cvv}
10. Complete Order.
11. If there's a verification code sent to {email}, use the skill to fetch it and enter it.
12. Confirm if the order was successful and provides an Order Number or Invoice.
"""

    print("Starting VPS purchase task...")
    result = browser_subagent(task)
    print(f"Result: {result.get('status')} | {result.get('output')}")


if __name__ == "__main__":
    main()
