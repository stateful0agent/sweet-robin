import os, requests, json, sys, re, subprocess
from datetime import datetime
from functions.browser_use import browser_subagent

# Load .env manually since we're adding to it at runtime
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


def list_unread(limit=20):
    address = os.environ["AGENTMAIL_ADDRESS"]
    r = requests.get(
        f"{API}/inboxes/{address}/messages?labels=unread&limit={limit}", headers=HDR
    )
    r.raise_for_status()
    return r.json()["messages"]


def get_message(message_id):
    address = os.environ["AGENTMAIL_ADDRESS"]
    # We need to URL encode the message_id as it might contain < > @ etc.
    from urllib.parse import quote_plus

    encoded_id = quote_plus(message_id)
    r = requests.get(f"{API}/inboxes/{address}/messages/{encoded_id}", headers=HDR)
    r.raise_for_status()
    return r.json()


def mark_read(message_id):
    address = os.environ["AGENTMAIL_ADDRESS"]
    from urllib.parse import quote_plus

    encoded_id = quote_plus(message_id)
    try:
        # Patch to remove unread label or just set labels
        r = requests.patch(
            f"{API}/inboxes/{address}/messages/{encoded_id}",
            headers=HDR,
            json={"labels": ["received"]},
        )
        print(f"Mark read {message_id}: {r.status_code} {r.text}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error marking read: {e}")
        return False


def get_balance():
    try:
        r = requests.get(
            "https://ai-gateway.vercel.sh/v1/credits",
            headers={"Authorization": f"Bearer {os.environ['AI_GATEWAY_API_KEY']}"},
        )
        r.raise_for_status()
        return f"${r.json()['balance']}"
    except:
        return "Unknown"


def handle_activation(msg, full_msg):
    body = full_msg.get("text", "")
    html = full_msg.get("html", "")
    content = body + html
    # Try multiple patterns for activation/confirmation links
    patterns = [
        r'https://console\.cron-job\.org/confirmAccount/[^\s"\'<>]+',
        r'https://[^\s"\'<>]*namecheap\.com[^\s"\'<>]*verify[^\s"\'<>]*',
        r'https://[^\s"\'<>]*namecheap\.com[^\s"\'<>]*confirm[^\s"\'<>]*',
        r'https://[^\s"\'<>]*porkbun\.com[^\s"\'<>]*verify[^\s"\'<>]*',
        r'https://[^\s"\'<>]*porkbun\.com[^\s"\'<>]*reset[^\s"\'<>]*',
    ]
    for pattern in patterns:
        links = re.findall(pattern, content)
        if links:
            link = links[0]
            print(f"Activating account: {link}")
            result = browser_subagent(
                f"Visit this URL to activate or confirm the account: {link}", url=link
            )
            return f"Activation result: {result}"
    return None


def process_command(sender, subject, body):
    # Extract email from "Name <email@example.com>"
    email_match = re.search(r"<(.+?)>", sender)
    sender_email = email_match.group(1) if email_match else sender

    # Security Check
    allowed = os.environ.get("ALLOWED_SENDERS", "").split(",")
    is_allowed = sender_email in allowed

    # Search for COMMAND: in subject or body
    match = re.search(r"COMMAND:\s*(\w+)\s*(.*)", subject + " " + body, re.IGNORECASE)
    if not match:
        return None

    cmd = match.group(1).upper()
    args = match.group(2).strip()

    # Only allow SUBSCRIBE and UNSUBSCRIBE for everyone
    if cmd not in ["SUBSCRIBE", "UNSUBSCRIBE"] and not is_allowed:
        print(f"Blocked command {cmd} from unauthorized sender: {sender_email}")
        return None
    print(f"Processing command {cmd} from {sender}")

    if cmd == "STATUS":
        balance = get_balance()
        today = datetime.now().strftime("%Y-%m-%d")
        return f"Balance: {balance}. System online. Date: {today}."
    elif cmd == "SUBSCRIBE":
        with open("subscribers.json", "r") as f:
            subscribers = json.load(f)
        if sender_email not in subscribers:
            subscribers.append(sender_email)
            with open("subscribers.json", "w") as f:
                json.dump(subscribers, f, indent=2)
            return f"Subscribed: {sender_email}"
        else:
            return f"Already subscribed: {sender_email}"
    elif cmd == "UNSUBSCRIBE":
        with open("subscribers.json", "r") as f:
            subscribers = json.load(f)
        if sender_email in subscribers:
            subscribers.remove(sender_email)
            with open("subscribers.json", "w") as f:
                json.dump(subscribers, f, indent=2)
            return f"Unsubscribed: {sender_email}"
        else:
            return f"Not subscribed: {sender_email}"
    elif cmd == "REMOVE":
        try:
            with open("TODO.md", "r") as f:
                lines = f.readlines()
            new_lines = []
            removed = False
            for line in lines:
                if args.lower() in line.lower() and not removed:
                    removed = True
                    continue
                new_lines.append(line)
            with open("TODO.md", "w") as f:
                f.writelines(new_lines)
            if removed:
                return f"Removed from TODO: {args}"
            else:
                return f"Not found in TODO: {args}"
        except Exception as e:
            return f"Error removing from TODO: {str(e)}"
    elif cmd == "BRAINSTORM":
        today = datetime.now().strftime("%Y-%m-%d")
        journal_path = f"journal/{today}.md"
        if not os.path.exists(journal_path):
            with open(journal_path, "w") as f:
                f.write(f"# {today}\n\n")
        with open(journal_path, "a") as f:
            f.write(f"\n### Brainstorm Idea (via email)\n{args}\n")
        return f"Added to journal brainstorm: {args}"
    elif cmd == "READ":
        try:
            with open(args, "r") as f:
                content = f.read()
            return f"Content of {args}:\n\n{content}"
        except Exception as e:
            return f"Error reading {args}: {str(e)}"
    elif cmd == "RUN":
        try:
            # Only allow running scripts/ or other safe commands?
            # For now, let's just use subprocess
            result = subprocess.run(
                args, shell=True, capture_output=True, text=True, timeout=30
            )
            return f"Run result for '{args}':\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        except Exception as e:
            return f"Error running '{args}': {str(e)}"
    else:
        return f"Unknown command: {cmd}"


def main():
    processed_file = "processed_messages.json"
    if os.path.exists(processed_file):
        with open(processed_file, "r") as f:
            processed = set(json.load(f))
    else:
        processed = set()

    messages = list_unread()
    print(f"Found {len(messages)} unread messages.")
    for msg in messages:
        mid = msg["message_id"]
        if mid in processed:
            continue

        sender = msg.get("from", "")
        subject = msg.get("subject", "")
        print(f"Processing '{subject}' from '{sender}'")

        full_msg = get_message(mid)

        # Check for activation links first
        activation_result = handle_activation(msg, full_msg)
        if activation_result:
            # Send result back?
            requests.post(
                f"{API}/inboxes/{os.environ['AGENTMAIL_ADDRESS']}/messages/send",
                headers=HDR,
                json={
                    "to": sender,
                    "subject": f"RE: {subject}",
                    "text": activation_result,
                },
            )
            mark_read(mid)
            processed.add(mid)
            continue

        # Check for commands
        body = full_msg.get("text", "")
        response = process_command(sender, subject, body)
        if response:
            # Send response back
            requests.post(
                f"{API}/inboxes/{os.environ['AGENTMAIL_ADDRESS']}/messages/send",
                headers=HDR,
                json={"to": sender, "subject": f"RE: {subject}", "text": response},
            )
            print(f"Responded to {sender}")
            mark_read(mid)
        else:
            # If not a command and not handled, still mark as read?
            # Let's mark as read to avoid re-processing if possible.
            mark_read(mid)

        processed.add(mid)

    # Save processed set
    with open(processed_file, "w") as f:
        json.dump(list(processed), f)


if __name__ == "__main__":
    main()
