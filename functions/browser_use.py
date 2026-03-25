import json, os, time, requests

API = "https://api.browser-use.com/api/v2"
HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}

ACCOUNTS_SKILL = """
NOTE: For logging into sites, prefer Google SSO (your browser profile is already logged into Google).
If Google login is unavailable or fails, login/create an account using:
  Email: {agentmail_address}
  Password: {agentmail_password}"""

EMAIL_SKILL = """
NOTE: If any site asks for an email verification code, you can retrieve it via HTTP:
  GET https://api.agentmail.to/v0/inboxes/{inbox_id}/messages?limit=3
  Header: Authorization: Bearer {api_key}
The response JSON has a "messages" array. Each message has "subject" and "preview" fields containing the code."""


def browser_subagent(task: str, url: str | None = None) -> dict:
    address = os.environ.get("AGENTMAIL_ADDRESS", "")
    api_key = os.environ.get("AGENTMAIL_API_KEY", "")
    password = os.environ.get("AGENTMAIL_PASSWORD", "")

    if address and password:
        task += ACCOUNTS_SKILL.format(agentmail_address=address, agentmail_password=password)
    if address and api_key:
        task += EMAIL_SKILL.format(inbox_id=address, api_key=api_key)

    settings = {"profileId": os.environ.get("BROWSER_USE_PROFILE_ID")}
    proxy_host = os.environ.get("PROXY_HOST")
    if proxy_host:
        settings["customProxy"] = {
            "host": proxy_host,
            "port": int(os.environ["PROXY_PORT"]),
            "username": os.environ["PROXY_USER"],
            "password": os.environ["PROXY_PASS"],
        }
    else:
        settings["proxyCountryCode"] = "us"

    body = {"task": task, "sessionSettings": settings}
    if url:
        body["startUrl"] = url

    tid = requests.post(f"{API}/tasks", json=body, headers=HDR).json()["id"]
    print(f"Task {tid} started")

    while True:
        time.sleep(5)
        if requests.get(f"{API}/tasks/{tid}/status", headers=HDR).json()["status"] in ("finished", "stopped"):
            break

    detail = requests.get(f"{API}/tasks/{tid}", headers=HDR).json()
    os.makedirs("browser-use-traces", exist_ok=True)
    json.dump(detail, open(f"browser-use-traces/{tid}.json", "w"), indent=2)
    print(f"{detail['status']} | {detail.get('output', 'None')}")
    return detail
