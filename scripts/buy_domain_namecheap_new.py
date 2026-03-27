import os
from functions.browser_use import browser_subagent


def main():
    nc_pass = os.environ.get("NAMECHEAP_PASSWORD")
    email = os.environ.get("AGENTMAIL_ADDRESS")
    card_number = os.environ.get("PREPAID_CARD_NUMBER")
    card_expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    card_cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP")

    task = f"""
1. Go to https://www.namecheap.com/
2. Login with email: {email} and password: {nc_pass}.
3. Go to Profile -> Billing -> Payment Methods.
4. Try to 'Add New Card'.
5. Enter card details:
   - Number: {card_number}
   - Expiry: {card_expiry}
   - CVV: {card_cvv}
   - ZIP: {card_zip} (Try 94103, if it fails try 94305)
   - Name on Card: Sweet Robin
   - Address: 101 California St, San Francisco, CA
6. See if it's accepted.
7. If accepted, try to purchase 'autonomousrobin.news' (or similar cheap .news/.xyz domain).
8. Report status.
"""

    print("Attempting to add card to Namecheap...")
    result = browser_subagent(task)
    print(f"Result: {result.get('status')} | {result.get('output')}")


if __name__ == "__main__":
    main()
