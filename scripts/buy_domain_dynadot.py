import sys
import os
from functions.browser_use import browser_subagent

def main():
    password = os.environ.get("NAMECHEAP_PASSWORD")
    if not password:
        print("NAMECHEAP_PASSWORD not found in .env")
        sys.exit(1)

    domain = "autonomousrobin.news"
    # Use the password, email, and verification code provided by the user
    email = "sweet.robin.163@agentmail.to"
    verification_code = "720630"
    
    task = f"""
Go to https://www.dynadot.com
1. Click 'Sign In' (usually at the top right).
2. Login with email '{email}' and password '{password}'.
3. If prompted for a verification code (e.g. for 2FA or device login), use '{verification_code}'.
4. Once logged in, search for the domain '{domain}'.
5. If '{domain}' is available or in the cart, add it to the cart if it's not already there.
6. Proceed to the checkout/cart page.
7. Set up the payment method using this Vanilla Visa card:
   - Card Number: 4511292827172591
   - Expiry: 02/35
   - CVV: 492
   - Billing ZIP Code: 94103
   - Billing address: You can use a generic San Francisco address if needed, like '123 Market St, San Francisco, CA 94103'.
8. Attempt to complete the order.
9. Report if the purchase was successful or what the error was. If the card is declined, please state that clearly.
"""

    print(f"Starting browser task to buy {domain} on Dynadot...")
    # The browser_subagent function will use the BROWSER_USE_API_KEY from .env
    result = browser_subagent(task, url="https://www.dynadot.com")
    
    if result.get("status") == "finished":
        print("\nTask Output:")
        print(result.get("output", "No output returned"))
    else:
        print(f"\nTask failed with status: {result.get('status')}")
        print(f"Error: {result.get('output', 'Unknown error')}")

if __name__ == "__main__":
    main()
