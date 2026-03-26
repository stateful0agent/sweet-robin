import os, requests, json, sys
from urllib.parse import quote_plus

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


def get_message(message_id):
    address = os.environ["AGENTMAIL_ADDRESS"]
    encoded_id = quote_plus(message_id)
    r = requests.get(f"{API}/inboxes/{address}/messages/{encoded_id}", headers=HDR)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/read_mail.py <message_id>")
        sys.exit(1)

    msg = get_message(sys.argv[1])
    print(json.dumps(msg, indent=2))
