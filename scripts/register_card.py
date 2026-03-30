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
    2. Click 'Check Balance'.
    3. If you see a "Checking if you're a human" or a blank page, WAIT at least 60 seconds. 
    4. Try to click anywhere on the page to trigger the Cloudflare checkbox.
    5. Once you see the card entry fields, enter:
       - Card Number: {card_number}
       - Expiration Date: {card_expiry}
       - CVV: {card_cvv}
    6. Click 'Sign In' or 'Check Balance'.
    7. Once logged in, go to 'Manage Card' or 'Edit Profile'.
    8. Look for 'Assign ZIP Code'.
    9. Set the ZIP code to: {card_zip}
    10. Confirm and report success.
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
