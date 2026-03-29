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

    card_number = os.environ.get("PREPAID_CARD_NUMBER", "")
    card_expiry = os.environ.get("PREPAID_CARD_EXPIRY", "")
    card_cvv = os.environ.get("PREPAID_CARD_CVV", "")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    if not all([card_number, card_expiry, card_cvv]):
        print("Missing card details in .env")
        return

    task = f"""
    1. Go to https://www.vanillagift.com/
    2. Look for 'Check Balance' or 'Manage Card'.
    3. Enter the card details:
       - Card Number: {card_number}
       - Expiration Date: {card_expiry} (Format might be MM/YY or MM/YYYY, handle accordingly)
       - CVV: {card_cvv}
    4. Once logged in, look for an option to 'Assign ZIP Code' or 'Register for Online Purchases' or 'Edit Profile'.
    5. Set the ZIP code to: {card_zip}
    6. Confirm the registration.
    7. Tell me if it was successful.
    """

    print("Starting card registration on vanillagift.com...")
    # Masking sensitive info in the printed task for logs (though browser_subagent will see the real one)
    masked_task = task.replace(card_number if card_number else "****", "****").replace(
        card_cvv if card_cvv else "***", "***"
    )
    # print(masked_task) # Don't even print the masked task to be safe, just run it.

    result = browser_subagent(task, url="https://www.vanillagift.com/")
    print(f"Result: {result.get('output')}")


if __name__ == "__main__":
    main()
