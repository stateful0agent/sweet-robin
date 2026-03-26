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

    task = f"""
    Go to Namecheap.com and search for '{domain}'.
    If blocked by Cloudflare, wait 20s or click verify human.
    If available, add to cart and checkout.
    Log in with username '{username}' and password '{password}'.
    Payment details: Card {card_number}, CVV {card_cvv}, Exp {card_expiry}, Zip {zip_code}.
    Name: Sweet Robin. Address: 123 Main St, San Francisco, CA 94103.
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
        "startUrl": "https://www.namecheap.com/domains/registration/results/?domain="
        + domain,
    }

    print(f"Starting task to buy {domain} on Namecheap...")
    resp = requests.post(f"{API}/tasks", json=body, headers=HDR)
    if resp.status_code == 201:
        tid = resp.json()["id"]
        print(
            f"Task {tid} started. Poll it with `uv run scripts/check_browser_task.py {tid}`"
        )
    else:
        print(f"Failed to start task: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    main()
