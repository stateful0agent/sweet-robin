import sys
import os
from functions.browser_use import browser_subagent


def buy_domain_namesilo_paypal_guest(domain):
    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")
    email = os.getenv("AGENTMAIL_ADDRESS")

    task = f"""
    Go to https://www.namesilo.com
    1. Search for '{domain}' and add to cart.
    2. Go to Checkout.
    3. Choose 'PayPal' as payment method.
    4. When PayPal opens, click 'Pay with Debit or Credit Card' or 'Checkout as Guest'.
    5. Enter card details:
       - Card: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
       - Billing ZIP: {card_zip}
       - Email: {email}
    6. Complete the order.
    7. If it asks to create a PayPal account, try to skip it.
    8. Report status.
    """

    print(f"Attempting to buy {domain} on NameSilo via PayPal Guest...")
    result = browser_subagent(task, url="https://www.namesilo.com")
    return result


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "autonomousrobin.news"
    res = buy_domain_namesilo_paypal_guest(domain)
    print(res.get("output", "No output from browser agent."))
