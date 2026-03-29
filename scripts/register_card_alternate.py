import os
import sys
from functions.browser_use import browser_subagent


def register_card_alternate(url):
    card_number = os.environ.get("PREPAID_CARD_NUMBER", "")
    card_expiry = os.environ.get("PREPAID_CARD_EXPIRY", "")
    card_cvv = os.environ.get("PREPAID_CARD_CVV", "")
    card_zip = os.environ.get("PREPAID_CARD_ZIP", "94103")

    task = f"""
    1. Go to {url}
    2. Look for 'Assign ZIP' or 'Check Balance' or 'Manage Card'.
    3. Enter: {card_number}, {card_expiry}, {card_cvv}.
    4. If it works, set ZIP to {card_zip}.
    5. Tell me if successful.
    """

    print(f"Trying to register on {url}...")
    result = browser_subagent(task, url=url)
    return result


if __name__ == "__main__":
    urls = ["https://www.vanillabalance.com/", "https://www.myvanillacard.com/"]
    for url in urls:
        res = register_card_alternate(url)
        print(f"URL: {url} | Result: {res.get('output', 'No output')}")
