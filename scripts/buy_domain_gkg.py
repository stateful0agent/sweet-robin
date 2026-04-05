import os
import sys
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

    card_number = os.environ.get("PREPAID_CARD_NUMBER")
    card_expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    card_cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    task = f"""
    1. Go to https://www.gkg.net/
    2. Search for '{domain}' and add to cart.
    3. Go to Checkout.
    4. If you need an account, create one using:
       - Email: {email}
       - Password: StrongPassGKG2026!#
       - Name: Sweet Robin
       - Address: 123 Main St, San Francisco, CA 94103
    5. In the payment section, select 'Credit Card'.
    6. Enter:
       - Number: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
    7. Ensure ZIP is {card_zip}.
    8. Attempt to complete order.
    9. GKG often allows checkout without AVS. If it fails, report the error message.
    """

    print(f"Attempting to buy {domain} on GKG.net...")
    result = browser_subagent(task, url="https://www.gkg.net/")
    print(result.get("output"))


if __name__ == "__main__":
    main()
