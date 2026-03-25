import argparse, os, requests, json

API = "https://api.agentmail.to/v0"
HDR = {
    "Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}",
    "Content-Type": "application/json",
}


def list_messages(limit=10):
    address = os.environ["AGENTMAIL_ADDRESS"]
    r = requests.get(f"{API}/inboxes/{address}/messages?limit={limit}", headers=HDR)
    r.raise_for_status()
    messages = r.json()
    return messages


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=10)
    args = p.parse_args()

    messages = list_messages(args.limit)
    print(json.dumps(messages, indent=2))
