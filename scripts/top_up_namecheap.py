import os
import sys
from functions.browser_use import browser_subagent


def top_up_namecheap(amount):
    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")
    email = "sweet.robin.163@agentmail.to"
    namecheap_pass = os.getenv("NAMECHEAP_PASSWORD")

    task = f"""
    1. Go to https://www.namecheap.com/myaccount/login/
    2. Login with username: {email} and password: {namecheap_pass}
    3. If there is 2FA:
       - 2FA should be sent to {email}.
       - Use your skill to get the code from AgentMail or just wait and look for it in the inbox if you can. 
       Actually, you should check AgentMail (https://agentmail.to/) yourself.
    4. Once logged in, go to 'Top-up Account Balance' or similar (usually under 'Billing').
    5. Choose 'Card' as the payment method.
    6. Enter the amount: ${amount}
    7. Enter card details:
       - Card: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
       - Billing ZIP: {card_zip}
       - Name: Sweet Robin
       - Address: 123 Main St, San Francisco, CA 94103
    8. Complete the top-up.
    9. Report status and current balance.
    """

    print(f"Attempting to top up Namecheap balance with ${amount}...")
    result = browser_subagent(task, url="https://www.namecheap.com/myaccount/login/")
    return result


if __name__ == "__main__":
    amount = sys.argv[1] if len(sys.argv) > 1 else "15"
    res = top_up_namecheap(amount)
    print(res.get("output", "No output from browser agent."))
