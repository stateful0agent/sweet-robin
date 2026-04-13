import os
import sys
from functions.browser_use import browser_subagent


def main():
    domain = "autonomousrobin.news"
    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")
    email = "sweet.robin.163@agentmail.to"

    task = f"""
    1. Go to https://www.namesilo.com/domain/search
    2. Search for '{domain}'.
    3. Add it to the cart and proceed to checkout.
    4. At checkout, select 'PayPal' as the payment method.
    5. When PayPal opens, click 'Pay with Debit or Credit Card' or 'Checkout as Guest'.
    6. Enter card details: {card_number}, {card_expiry}, {card_cvv}, {card_zip}.
    7. Complete the purchase.
    """

    print(f"Attempting to resume NameSilo purchase for {domain}...")
    result = browser_subagent(task, url="https://www.namesilo.com/domain/search")
    print(f"Status: {result.get('status')}")
    print("Result:", result.get("output"))


if __name__ == "__main__":
    main()
