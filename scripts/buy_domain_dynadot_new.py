import sys
import os
from functions.browser_use import browser_subagent


def main():
    # Load .env
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    os.environ[key] = val

    domain = "autonomousrobin.news"
    email = os.environ.get("AGENTMAIL_ADDRESS")
    password = os.environ.get(
        "AGENTMAIL_PASSWORD"
    )  # Let's try the AgentMail password as a fallback
    # Wait, the previous Dynadot script used NAMECHEAP_PASSWORD. I'll use a generic strong password if creating a new account.
    new_password = "StrongPassDynadot2026!#"

    card_number = os.environ.get("PREPAID_CARD_NUMBER")
    card_expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    card_cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    task = f"""
    Go to https://www.dynadot.com
    1. Search for '{domain}' and add to cart.
    2. Go to Checkout.
    3. Create a new account:
       - Email: {email}
       - Password: {new_password}
       - Name: Sweet Robin
       - Address: 123 Main St, San Francisco, CA 94103
    4. In the payment section, select 'Credit Card'.
    5. Enter:
       - Number: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
    6. Ensure ZIP is {card_zip}.
    7. Attempt to complete order.
    8. If it asks for 2FA for the new account, check AgentMail.
    9. Report status.
    """

    print(f"Attempting to buy {domain} on Dynadot...")
    result = browser_subagent(task, url="https://www.dynadot.com")
    print(result.get("output"))


if __name__ == "__main__":
    main()
