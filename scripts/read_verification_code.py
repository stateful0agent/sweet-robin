import os
import requests
import json
import re

API = "https://api.agentmail.to/v0"
HDR = {"Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}"}
EMAIL = os.environ["AGENTMAIL_ADDRESS"]


def get_messages():
    resp = requests.get(f"{API}/inboxes/{EMAIL}/messages?limit=100", headers=HDR)
    if resp.status_code == 200:
        msgs = resp.json()["messages"]
        for m in msgs:
            if "namecheap" in m["from"].lower() or "namecheap" in m["subject"].lower():
                print(
                    f"Subject: {m['subject']} | From: {m['from']} | Labels: {m.get('labels')}"
                )
                if (
                    "confirmation code" in m["subject"].lower()
                    and "RE:" not in m["subject"]
                ):
                    print(f"Preview: {m.get('preview')}")
                    mid = m["message_id"]
                    from urllib.parse import quote_plus

                    emid = quote_plus(mid)
                    r2 = requests.get(
                        f"{API}/inboxes/{EMAIL}/messages/{emid}", headers=HDR
                    )
                    if r2.status_code == 200:
                        mdata = r2.json()
                        html = mdata.get("html", "")
                        print(f"FULL HTML: {html}")

                print("-" * 20)

    else:
        print(f"Error: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    get_messages()
