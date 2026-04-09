import os
import sys
from functions.browser_use import browser_subagent


def buy_domain_namesilo_v2(domain):
    email = "sweet.robin.163@agentmail.to"
    password = os.environ.get("NAMESILO_PASSWORD")
    card_num = os.environ.get("PREPAID_CARD_NUMBER")
    expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    task = f"""
    1. Go to https://www.namesilo.com/login and log in.
       - Email: {email}
       - Password: {password}
    2. If it asks for a 'New device authorization' code:
       - Use the AgentMail API (GET https://api.agentmail.to/v0/inboxes/{email}/messages?limit=5) 
         with the Authorization: Bearer <your_api_key_from_skill> header to find the code.
       - DO NOT try to log in to the AgentMail UI if you can use the API.
    3. Once logged in, search for '{domain}'.
    4. Add it to the cart (or if already in cart, proceed).
    5. Go to Checkout.
    6. Select 'Credit Card' as payment.
    7. Enter:
       - Card: {card_num}
       - Exp: {expiry}
       - CVV: {cvv}
       - ZIP: {card_zip}
       - Name: Sweet Robin
       - Address: 123 Main St, San Francisco, CA {card_zip}
    8. Attempt to complete purchase.
    9. Report Success/Failure and any error messages.
    """

    print(f"NameSilo V2 purchase for {domain}...")
    result = browser_subagent(task, url="https://www.namesilo.com/login")
    return result


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "autonomousrobin.news"
    res = buy_domain_namesilo_v2(domain)
    if res:
        print(f"Result: {res.get('status')} | {res.get('output', 'No output')}")
