import os, requests, json

if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                os.environ[key] = val

API = "https://api.agentmail.to/v0"
HDR = {
    "Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}",
    "Content-Type": "application/json",
}


def find_porkbun_code():
    address = os.environ["AGENTMAIL_ADDRESS"]
    r = requests.get(f"{API}/inboxes/{address}/messages?limit=50", headers=HDR)
    r.raise_for_status()
    messages = r.json()["messages"]

    for msg in messages:
        if (
            "Account Creation Email Verification Code" in msg["subject"]
            and "received" in msg["labels"]
        ):
            # Get full message
            from urllib.parse import quote_plus

            encoded_id = quote_plus(msg["message_id"])
            mr = requests.get(
                f"{API}/inboxes/{address}/messages/{encoded_id}", headers=HDR
            )
            full_msg = mr.json()
            body = full_msg.get("text", "")
            # Look for 6 digit code
            import re

            match = re.search(r"\b(\d{6})\b", body)
            if match:
                return match.group(1), msg["timestamp"]
    return None, None


if __name__ == "__main__":
    code, ts = find_porkbun_code()
    if code:
        print(f"Latest Porkbun code: {code} (from {ts})")
    else:
        print("No Porkbun code found.")
