import os
import requests
import json
import re
import sys

API = "https://api.agentmail.to/v0"
HDR = {"Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}"}
EMAIL = os.environ["AGENTMAIL_ADDRESS"]


def get_messages(search_term="namecheap"):
    resp = requests.get(f"{API}/inboxes/{EMAIL}/messages?limit=100", headers=HDR)
    if resp.status_code == 200:
        msgs = resp.json()["messages"]
        for m in msgs:
            if (
                search_term.lower() in m["from"].lower()
                or search_term.lower() in m["subject"].lower()
            ):
                print(
                    f"Subject: {m['subject']} | From: {m['from']} | Labels: {m.get('labels')}"
                )
                mid = m["message_id"]
                from urllib.parse import quote_plus

                emid = quote_plus(mid)
                r2 = requests.get(f"{API}/inboxes/{EMAIL}/messages/{emid}", headers=HDR)
                if r2.status_code == 200:
                    mdata = r2.json()
                    html = mdata.get("html", "")
                    # Extract 6-digit code or anything similar, but exclude common numbers like 222222 or years
                    codes = re.findall(r"\b\d{6}\b", html)
                    # Also check for alphanumeric codes (like Namecheap's sometimes are)
                    codes += re.findall(r"\b[A-Za-z0-9]{6}\b", html)

                    # Filter out obviously wrong ones
                    valid_codes = []
                    for c in codes:
                        if c not in ("222222", "123456", "000000"):
                            if not re.match(r"^(19|20)\d{2}$", c):  # Not a year
                                valid_codes.append(c)

                    if valid_codes:
                        # Print unique codes
                        print(f"CODES FOUND: {list(set(valid_codes))}")
                    else:
                        print("No valid codes found.")

                print("-" * 20)

    else:
        print(f"Error: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    term = sys.argv[1] if len(sys.argv) > 1 else "namecheap"
    get_messages(term)
