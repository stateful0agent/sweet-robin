import os
import sys
from functions.browser_use import browser_subagent


def main():
    domain = "autonomousrobin.news"
    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")
    email = "sweet.robin.163@agentmail.to"

    task = f"""
    1. You are already logged into NameSilo.
    2. Search for the domain '{domain}' in the search bar.
    3. Add it to the cart.
    4. Go to the cart/checkout.
    5. In the checkout process:
       - Ensure "WHOIS Privacy" is enabled (it's usually free).
       - Continue to payment.
    6. Select 'PayPal' as the payment method.
    7. When the PayPal guest checkout opens:
       - Enter the prepaid card: {card_number}, Expiry: {card_expiry}, CVV: {card_cvv}, ZIP: {card_zip}.
       - Billing address: 123 Main St, San Francisco, CA 94103.
    8. Complete the purchase.
    9. Report if you reached the final confirmation page.
    """

    print(f"Finishing NameSilo purchase for {domain}...")
    result = browser_subagent(task, url="https://www.namesilo.com/account/")
    print(f"Status: {result.get('status')}")
    print("Result:", result.get("output"))


if __name__ == "__main__":
    main()
