import sys
from functions.browser_use import browser_subagent


def buy_domain_namesilo(domain, email, password, card_num, expiry, cvv, name, address):
    task = f"""
    Go to NameSilo.com and search for '{domain}'.
    Add '{domain}' to the cart and proceed to checkout.
    Create a new account:
    Email: {email}
    Password: {password}
    
    If an account already exists or after creating one:
    In the payment section, select 'Credit Card'.
    Enter:
    Card Number: {card_num}
    Expiry: {expiry}
    CVV: {cvv}
    Billing Name: {name}
    Billing Address: {address}
    
    Attempt to complete the purchase. 
    If successful, report the order ID. 
    If it fails, report the error message displayed on the site.
    """

    result = browser_subagent(task, url="https://www.namesilo.com")
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/buy_domain_namesilo.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    # These should ideally be secrets or passed via args, but for this specific instruction,
    # the user provided them directly.
    email = "sweet.robin.163@agentmail.to"
    password = "StrongPassNameSilo2026!"
    card_num = "4511292827172591"
    expiry = "02/35"
    cvv = "492"
    name = "Sweet Robin"
    address = "123 Main St, San Francisco, CA 94103"

    res = buy_domain_namesilo(
        domain, email, password, card_num, expiry, cvv, name, address
    )
    print(res.get("output", "No output from browser agent"))
