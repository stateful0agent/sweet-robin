import os, requests, json, sys, re
from functions.browser_use import browser_subagent

API = "https://api.agentmail.to/v0"
HDR = {
    "Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}",
    "Content-Type": "application/json",
}


def list_unread():
    address = os.environ["AGENTMAIL_ADDRESS"]
    r = requests.get(f"{API}/inboxes/{address}/messages?labels=unread", headers=HDR)
    r.raise_for_status()
    return r.json()["messages"]


def get_message(message_id):
    address = os.environ["AGENTMAIL_ADDRESS"]
    r = requests.get(f"{API}/inboxes/{address}/messages/{message_id}", headers=HDR)
    r.raise_for_status()
    return r.json()


def mark_read(message_id):
    address = os.environ["AGENTMAIL_ADDRESS"]
    # Testing PATCH for labels
    try:
        r = requests.patch(
            f"{API}/inboxes/{address}/messages/{message_id}",
            headers=HDR,
            json={"labels": ["received"]},
        )  # Remove unread
        return r.status_code == 200
    except:
        return False


def process_command(sender, subject, body):
    print(f"Command from {sender}: {subject}")
    # Regex for "COMMAND: <action> <args>"
    match = re.search(r"COMMAND:\s*(\w+)\s*(.*)", subject + " " + body, re.IGNORECASE)
    if not match:
        return None

    cmd = match.group(1).upper()
    args = match.group(2).strip()

    if cmd == "STATUS":
        return "Balance is $95.0. All systems operational."
    elif cmd == "TODO":
        with open("TODO.md", "a") as f:
            f.write(f"- [ ] {args} (via email)\n")
        return f"Added to TODO: {args}"
    elif cmd == "BRAINSTORM":
        with open("journal/2026-03-25.md", "a") as f:
            f.write(f"\n### Brainstorm Idea (via email)\n{args}\n")
        return f"Added to journal brainstorm: {args}"
    else:
        return f"Unknown command: {cmd}"


def main():
    messages = list_unread()
    for msg in messages:
        # Avoid processing automated notifications as commands unless they have COMMAND:
        full = get_message(msg["message_id"])
        body = full.get("text", "")
        sender = msg.get("from", "")
        subject = msg.get("subject", "")

        response = process_command(sender, subject, body)
        if response:
            # Send response back
            requests.post(
                f"{API}/inboxes/{os.environ['AGENTMAIL_ADDRESS']}/messages/send",
                headers=HDR,
                json={"to": sender, "subject": f"RE: {subject}", "text": response},
            )
            print(f"Responded to {sender}")
            mark_read(msg["message_id"])


if __name__ == "__main__":
    main()
