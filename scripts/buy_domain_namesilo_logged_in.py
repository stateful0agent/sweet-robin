import os
import sys
from functions.browser_use import browser_subagent


def buy_domain_namesilo(domain):
    email = "sweet.robin.163@agentmail.to"
    password = os.environ.get("NAMESILO_PASSWORD")
    card_num = os.environ.get("PREPAID_CARD_NUMBER")
    expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    if not all([password, card_num, expiry, cvv]):
        print("Missing NameSilo password or card details in .env")
        return None

    task = f"""
    1. Go to NameSilo.com and login if not already (Email: {email}, Password: {password}).
    2. Search for '{domain}' and add it to the cart.
    3. Proceed to checkout.
    4. Select 'Credit Card' as payment method.
    5. Enter card details:
       - Card Number: {card_num}
       - Expiry: {expiry}
       - CVV: {cvv}
       - Billing Name: Sweet Robin
       - Billing Address: 123 Main St, San Francisco, CA {card_zip}
    6. Complete the purchase.
    7. If successful, report the order ID.
    8. If it fails with a 3DS error or other, tell me the exact error.
    """

    print(f"Attempting to buy domain {domain} on NameSilo...")
    result = browser_subagent(task, url="https://www.namesilo.com")
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/buy_domain_namesilo_logged_in.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    res = buy_domain_namesilo(domain)
    if res:
        print(f"Result: {res.get('output', 'No output')}")
    else:
        print("No result from browser agent or task failed.")
