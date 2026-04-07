import sys
import os
from functions.browser_use import browser_subagent


def buy_domain_namesilo_paypal_guest(domain):
    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")
    email = "sweet.robin.163@agentmail.to"
    namesilo_pass = os.getenv("NAMESILO_PASSWORD")
    agentmail_pass = os.getenv("AGENTMAIL_PASSWORD")

    task = f"""
    1. Go to NameSilo.com and login if not already logged in.
       - Email: {email}
       - Password: {namesilo_pass}
    2. If it asks for device authorization:
       - Go to AgentMail (https://agentmail.to/)
       - Login with Address: {email} and Password: {agentmail_pass}
       - Get the 6-digit code from the latest support@namesilo.com email.
       - Enter it on NameSilo and submit.
    3. Search for '{domain}' and add to cart.
    4. Proceed to Checkout.
    5. In the payment section, select 'PayPal'.
    6. When PayPal opens, click 'Pay with Debit or Credit Card' or 'Checkout as Guest'.
    7. Enter card details:
       - Card: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
       - Billing ZIP: {card_zip}
       - Email: {email}
       - Name: Sweet Robin
       - Address: 123 Main St, San Francisco, CA 94103
    8. Complete the purchase.
    9. Report status.
    """

    print(f"Attempting to buy {domain} on NameSilo via PayPal Guest (with login)...")
    result = browser_subagent(task, url="https://www.namesilo.com/login")
    return result


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "autonomousrobin.news"
    res = buy_domain_namesilo_paypal_guest(domain)
    print(res.get("output", "No output from browser agent."))
