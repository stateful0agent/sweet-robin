import os
import sys
import time
from functions.browser_use import browser_subagent


def buy_domain_sav(domain):
    email = "sweet.robin.163@agentmail.to"
    password = "RobinStrongSav2026!#"
    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")

    task = f"""
    1. Go to https://www.sav.com/ and create an account.
       Email: {email}
       Password: {password}
    
    2. Once logged in (verify via email if needed, check AgentMail), search for the domain '{domain}'.
    3. Add it to the cart and proceed to checkout.
    4. In the payment section, select 'Credit Card'.
    5. Enter the card details:
       - Card Number: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
       - Billing ZIP: {card_zip}
       - Name on Card: Robin Agent
    6. Complete the purchase.
    7. Report the final status.
    """

    print(f"Attempting to buy domain '{domain}' on Sav.com...")
    result = browser_subagent(task, url="https://www.sav.com/signup")
    return result


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "autonomousrobin.news"
    res = buy_domain_sav(domain)
    if res:
        print(f"Result: {res.get('output', 'No output')}")
    else:
        print("No result from browser agent or task failed.")
