import sys
import os
from functions.browser_use import browser_subagent


def buy_domain_namesilo_paypal_guest(domain):
    card_number = os.getenv("PREPAID_CARD_NUMBER")
    card_expiry = os.getenv("PREPAID_CARD_EXPIRY")
    card_cvv = os.getenv("PREPAID_CARD_CVV")
    card_zip = os.getenv("PREPAID_CARD_ZIP", "94103")
    email = "sweet.robin.163@agentmail.to"
    namesilo_pass = os.getenv("NAMESILO_PASSWORD")
    agentmail_pass = os.getenv("AGENTMAIL_PASSWORD")

    # Try to get latest code from local script first
    import subprocess

    code = "UNKNOWN"
    try:
        res = subprocess.run(
            ["PYTHONPATH=.", "uv", "run", "scripts/list_mail.py", "--limit", "1"],
            capture_output=True,
            text=True,
        )
        import json

        data = json.loads(res.stdout)
        if data["messages"] and "namesilo" in data["messages"][0]["from"].lower():
            code = (
                data["messages"][0]["preview"].split("\n")[-2].strip()
            )  # Simple extraction
            if not code.isdigit():
                # try another way
                import re

                match = re.search(r"\b\d{6}\b", data["messages"][0]["preview"])
                if match:
                    code = match.group(0)
    except:
        pass

    task = f"""
    1. Go to NameSilo.com and login.
       - Email: {email}
       - Password: {namesilo_pass}
    2. If it asks for device authorization:
       - The code is likely '{code}'. If that doesn't work, go to https://agentmail.to/ and get a fresh one.
       - Enter it on NameSilo and submit.
...
    """

    print(f"Attempting to buy {domain} on NameSilo via PayPal Guest (with login)...")
    result = browser_subagent(task, url="https://www.namesilo.com/login")
    return result


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "autonomousrobin.news"
    res = buy_domain_namesilo_paypal_guest(domain)
    print(res.get("output", "No output from browser agent."))
