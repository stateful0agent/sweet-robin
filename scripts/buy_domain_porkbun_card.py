import os
import time
from functions.browser_use import browser_subagent


def buy_domain_porkbun_card(domain):
    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")
    email = os.getenv("AGENTMAIL_ADDRESS")
    password = os.getenv("PORKBUN_PASSWORD")

    task = f"""
    Go to https://porkbun.com and sign in with email '{email}' and password '{password}'.
    If you are already logged in, skip login.
    If you see a 2FA prompt, check the AgentMail inbox for a code from Porkbun.
    
    1. Search for the domain '{domain}' and add it to the cart.
    2. Go to the cart / checkout.
    3. In the payment section, select 'Credit Card'.
    4. Enter the card details:
       - Card Number: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
    5. Ensure the billing ZIP is {card_zip}.
    6. Attempt to complete the purchase.
    7. If the card is declined, try ZIP code 94305 just in case.
    8. Report the final status.
    """

    print(f"Attempting to buy domain '{domain}' on Porkbun via Direct Card...")
    result = browser_subagent(task, url="https://porkbun.com")
    return result


if __name__ == "__main__":
    import sys

    domain = sys.argv[1] if len(sys.argv) > 1 else "autonomousrobin.news"
    res = buy_domain_porkbun_card(domain)
    print(res.get("output", "No output from browser agent."))
