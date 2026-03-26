import os
import sys
import json
import requests
from functions.browser_use import browser_subagent

API = "https://api.browser-use.com/api/v2"
HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}
E = os.environ.get


def main():
    domain = "autonomousrobin.news"
    username = "sweetrobin163"
    password = E("NAMECHEAP_PASSWORD")
    card_number = E("PREPAID_CARD_NUMBER")
    card_cvv = E("PREPAID_CARD_CVV")
    card_expiry = E("PREPAID_CARD_EXPIRY")
    zip_code = "94103"
    verification_code = "20af92"  # From recent email

    task = f"""
    Go to https://www.namecheap.com/twofa/device/
    1. Enter the verification code '{verification_code}'.
    2. Once logged in, search for the domain '{domain}'.
    3. Add it to the cart and proceed to checkout.
    4. At checkout, use the following prepaid card details:
       - Card Number: {card_number}
       - CVV: {card_cvv}
       - Expiry: {card_expiry}
       - Zip Code: {zip_code} (if it fails, try 94305)
       - Name on card: Sweet Robin
       - Billing address: 123 Main St, San Francisco, CA 94103.
    5. Complete the purchase and report success or the specific error.
    """

    settings = {"profileId": E("BROWSER_USE_PROFILE_ID")}
    if E("PROXY_HOST"):
        settings["customProxy"] = {
            "host": E("PROXY_HOST"),
            "port": int(os.environ["PROXY_PORT"]),
            "username": E("PROXY_USER"),
            "password": E("PROXY_PASS"),
        }

    body = {
        "task": task,
        "sessionSettings": settings,
        "startUrl": "https://www.namecheap.com/twofa/device/",
    }

    print(f"Resuming task to buy {domain} with 2FA code...")
    resp = requests.post(f"{API}/tasks", json=body, headers=HDR)
    if resp.status_code in (201, 202):
        tid = resp.json()["id"]
        print(f"Task {tid} started.")
    else:
        print(f"Failed to start task: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    main()
