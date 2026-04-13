import os
import sys
from functions.browser_use import browser_subagent


def main():
    domain = "autonomousrobin.news"
    email = os.environ.get("AGENTMAIL_ADDRESS")
    password = os.environ.get("NAMESILO_PASSWORD")
    card_number = os.environ.get("PREPAID_CARD_NUMBER")
    card_expiry = os.environ.get("PREPAID_CARD_EXPIRY")
    card_cvv = os.environ.get("PREPAID_CARD_CVV")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    task = f"""
    1. Go to https://www.namesilo.com/login and login.
       Email: {email}
       Password: {password}
    
    2. If it asks for a device authorization code:
       - Use the AgentMail API or check the inbox for the latest code from support@namesilo.com.
       - The code is likely 6 or more digits.
       - Enter it and submit.
    
    3. Once logged in, go to the 'Basket' or search for '{domain}' and add to cart.
    
    4. Go to Checkout.
    
    5. Select 'PayPal' as the payment method.
    
    6. When the PayPal guest checkout / payment page appears:
       - Select 'Pay with Debit or Credit Card' (Guest Checkout).
       - Card: {card_number}
       - Expiry: {card_expiry}
       - CVV: {card_cvv}
       - ZIP: {card_zip}
       - Name: Robin Agent
       - Address: 123 Main St, San Francisco, CA 94103
       - Phone: 4155551234
    
    7. Complete the purchase.
    
    8. If successful, you should see a confirmation page.
    9. Report 'DOMAIN PURCHASED' if successful, otherwise describe the error.
    """

    print(f"Starting final domain purchase attempt for {domain}...")
    result = browser_subagent(task, url="https://www.namesilo.com/login")
    print(f"Status: {result.get('status')}")
    print("Result:", result.get("output"))


if __name__ == "__main__":
    main()
