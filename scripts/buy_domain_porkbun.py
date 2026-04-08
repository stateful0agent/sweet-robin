import os
import requests
import json

E = os.environ.get


def main():
    domain = "autonomousrobin.news"
    username = "sweetrobin163"
    password = E("PORKBUN_PASSWORD")
    card_number = E("PREPAID_CARD_NUMBER")
    card_cvv = E("PREPAID_CARD_CVV")
    card_expiry = E("PREPAID_CARD_EXPIRY")
    zip_code = "94103"

    API = "https://api.browser-use.com/api/v2"
    HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}

    task = f"""
    1. Go to porkbun.com and log in with username '{username}' and password '{password}'.
    2. If there is a 2FA or 'Device Not Recognized' check:
       - The code is sent to your email (sweet.robin.163@agentmail.to).
       - You MUST check your email using the AgentMail skill or by visiting https://agentmail.to/ (you are already logged in).
       - Look for an email from 'Porkbun' with the subject 'porkbun.com | 2FA Code'.
       - Extract the code and enter it.
    3. Search for the domain '{domain}'.
    4. Add it to your cart.
    4. Proceed to checkout.
    5. Ensure the payment method is set to Credit/Debit card.
    6. Enter card details: Card {card_number}, CVV {card_cvv}, Expiry {card_expiry}, ZIP {zip_code}.
    7. Use Name: Sweet Robin. Address: 123 Main St, San Francisco, CA 94103.
    8. Attempt to complete the purchase.
    9. Report the final result: success or specific error message.
    """

    from typing import Any

    settings: dict[str, Any] = {}
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
        "startUrl": "https://porkbun.com/account/login",
    }

    print(f"Starting task to buy {domain} on Porkbun...")
    resp = requests.post(f"{API}/tasks", json=body, headers=HDR)
    if resp.status_code in (201, 202):
        tid = resp.json()["id"]
        print(
            f"Task {tid} started. Poll it with `uv run scripts/check_browser_task.py {tid}`"
        )
    else:
        print(f"Failed to start task: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    main()
