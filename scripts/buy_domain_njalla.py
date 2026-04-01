import os
import sys
from functions.browser_use import browser_subagent


def buy_domain_njalla(domain):
    email = os.getenv("AGENTMAIL_ADDRESS")
    password = os.getenv(
        "AGENTMAIL_PASSWORD"
    )  # I set Njalla password to the same as AgentMail for now

    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")

    task = f"""
    1. Go to https://njal.la/ and log in with email '{email}' and password '{password}'.
    2. Search for the domain '{domain}'.
    3. If available, add it to the cart and proceed to checkout.
    4. When asked for payment, look for 'Credit Card' or 'Stripe'.
    5. Enter card details:
       - Number: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
    6. Ensure billing ZIP is {card_zip}.
    7. Complete the purchase.
    8. Report the final status and the domain's status in the dashboard.
    """

    print(f"Attempting to buy domain '{domain}' on Njalla...")
    result = browser_subagent(task, url="https://njal.la/")
    return result


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "autonomousrobin.news"
    res = buy_domain_njalla(domain)
    print(res.get("output", "No output from browser agent."))
