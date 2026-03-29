import os
import requests
import json
import re
import sys
from urllib.parse import quote_plus

API = "https://api.agentmail.to/v0"
HDR = {"Authorization": f"Bearer {os.environ.get('AGENTMAIL_API_KEY')}"}
EMAIL = os.environ.get("AGENTMAIL_ADDRESS")


def get_latest_code(sender_pattern):
    if not HDR["Authorization"] or not EMAIL:
        print("Missing AGENTMAIL_API_KEY or AGENTMAIL_ADDRESS")
        return None

    resp = requests.get(f"{API}/inboxes/{EMAIL}/messages?limit=20", headers=HDR)
    if resp.status_code != 200:
        print(f"Error fetching messages: {resp.status_code} {resp.text}")
        return None

    msgs = resp.json()["messages"]
    for m in msgs:
        if (
            sender_pattern.lower() in m["from"].lower()
            or sender_pattern.lower() in m["subject"].lower()
        ):
            mid = m["message_id"]
            emid = quote_plus(mid)
            r2 = requests.get(f"{API}/inboxes/{EMAIL}/messages/{emid}", headers=HDR)
            if r2.status_code == 200:
                mdata = r2.json()
                text = mdata.get("text", "")
                html = mdata.get("html", "")
                content = text + html

                # Find 6-digit numeric codes
                codes = re.findall(r"\b\d{6}\b", content)
                if codes:
                    return codes[0]

                # Find any numeric codes (4-8 digits)
                codes = re.findall(r"\b\d{4,8}\b", content)
                if codes:
                    return codes[0]

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/get_latest_code.py <sender_pattern>")
        sys.exit(1)

    pattern = sys.argv[1]
    code = get_latest_code(pattern)
    if code:
        print(code)
    else:
        print(f"No code found for {pattern}")
