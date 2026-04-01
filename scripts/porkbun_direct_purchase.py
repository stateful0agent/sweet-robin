import os
import sys
from functions.browser_use import browser_subagent


def buy_domain_porkbun(domain):
    email = os.getenv("AGENTMAIL_ADDRESS")
    password = os.getenv("PORKBUN_PASSWORD")

    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")

    task = f"""
    1. Log in to Porkbun with email '{email}' and password '{password}'.
    2. Go to the domain search and search for '{domain}'.
    3. Add it to the cart and click checkout.
    4. On the checkout page, click the 'Pay With Card' button (if not already selected).
    5. Enter the card details: {card_number}, {card_expiry}, {card_cvv}.
    6. Ensure the billing ZIP is {card_zip}.
    7. Click 'Complete Order'.
    8. If it asks for 2FA again, check AgentMail and enter the code.
    9. Report the exact error if it fails (e.g., 'AVS failure', 'Declined', etc.).
    """

    print(f"Direct checkout for '{domain}' on Porkbun...")
    result = browser_subagent(task, url="https://porkbun.com")
    return result


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "autonomousrobin.news"
    res = buy_domain_porkbun(domain)
    print(res.get("output", "No output from browser agent."))
