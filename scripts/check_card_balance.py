import os
import sys
from functions.browser_use import browser_subagent


def check_card_balance():
    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")

    if not all([card_number, card_expiry, card_cvv]):
        print("Missing card details in .env")
        return None

    task = f"""
    Go to https://www.vanillagift.com/ and check the balance of the card.
    1. Enter Card Number: {card_number}
    2. Enter Expiry: {card_expiry}
    3. Enter CVV: {card_cvv}
    4. If there is hCaptcha, try to solve it if possible, otherwise tell me 'CAPTCHA BLOCKED'.
    5. Report the balance if successful.
    """

    print("Attempting to check Vanilla Visa card balance...")
    result = browser_subagent(task, url="https://www.vanillagift.com/check-balance")
    return result


if __name__ == "__main__":
    res = check_card_balance()
    if res:
        print(f"Result: {res.get('output', 'No output')}")
    else:
        print("No result from browser agent.")
