import os, requests, json, re
from functions.browser_use import browser_subagent

API = "https://api.agentmail.to/v0"
HDR = {
    "Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}",
    "Content-Type": "application/json",
}


def list_messages(limit=10, labels=None):
    address = os.environ["AGENTMAIL_ADDRESS"]
    url = f"{API}/inboxes/{address}/messages?limit={limit}"
    if labels:
        url += f"&labels={labels}"
    r = requests.get(url, headers=HDR)
    r.raise_for_status()
    return r.json()["messages"]


def get_message(message_id):
    address = os.environ["AGENTMAIL_ADDRESS"]
    r = requests.get(f"{API}/inboxes/{address}/messages/{message_id}", headers=HDR)
    r.raise_for_status()
    return r.json()


def mark_as_read(message_id):
    address = os.environ["AGENTMAIL_ADDRESS"]
    # Trying common "patch/put" patterns for read status
    r = requests.patch(
        f"{API}/inboxes/{address}/messages/{message_id}",
        headers=HDR,
        json={"labels": ["received"]},
    )  # Remove "unread"?
    # Or maybe there's a specific endpoint
    # Let's skip this if it fails, and just use unread filtering in list_messages
    return r.status_code


def process_activation_email(msg):
    full_msg = get_message(msg["message_id"])
    body = full_msg.get("text", "")
    html = full_msg.get("html", "")

    # Simple regex to find cron-job.org activation links
    links = re.findall(
        r'https://console\.cron-job\.org/confirmAccount/[^\s"\'<>]+', body + html
    )
    if not links:
        print(f"No activation link found in message {msg['message_id']}")
        return False

    link = links[0]
    print(f"Found activation link: {link}")

    # Use browser to click the link
    print(f"Activating cron-job.org account via browser...")
    result = browser_subagent(
        f"Visit this URL to activate the account: {link}", url=link
    )
    print(f"Browser result: {result}")
    return True


if __name__ == "__main__":
    messages = list_messages(labels="unread")
    print(f"Found {len(messages)} unread messages.")

    for msg in messages:
        subject = msg.get("subject", "")
        print(f"Processing message: {subject}")

        if "Activate account" in subject or "cron-job.org" in subject:
            success = process_activation_email(msg)
            if success:
                print(f"Successfully processed activation email.")
                # mark_as_read(msg["message_id"])
        else:
            print(f"Skipping unknown message type.")
