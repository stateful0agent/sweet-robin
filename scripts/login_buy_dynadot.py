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
    username = "robinagent2026"
    password = "StrongPassDynadot2026!#"

    card_number = os.environ.get("PREPAID_CARD_NUMBER")
    card_expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    card_cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    task = f"""
    1. Go to https://www.dynadot.com/account/sign-in
    2. Log in with:
       - Username: {username}
       - Password: {password}
    3. If it asks for a verification code, check AgentMail (last code was 132776 but might have expired).
    4. Search for '{domain}' and add to cart.
    5. Go to Checkout.
    6. In the payment section, select 'Credit Card'.
    7. Enter:
       - Number: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
    8. Ensure ZIP is {card_zip}.
    9. Attempt to complete order.
    10. Report status.
    """

    print(f"Attempting to log in and buy {domain} on Dynadot...")
    result = browser_subagent(task, url="https://www.dynadot.com/account/sign-in")
    print(result.get("output"))


if __name__ == "__main__":
    main()
