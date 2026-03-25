import json, os, time, requests

API = "https://api.browser-use.com/api/v2"
HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}
E = os.environ.get

SKILLS = ""
if E("AGENTMAIL_ADDRESS") and E("AGENTMAIL_PASSWORD"):
    SKILLS += f"\nFor site logins: prefer Google SSO (profile is logged in). Fallback: email {E('AGENTMAIL_ADDRESS')} password {E('AGENTMAIL_PASSWORD')}"
if E("AGENTMAIL_ADDRESS") and E("AGENTMAIL_API_KEY"):
    SKILLS += f"\nFor email verification codes: GET https://api.agentmail.to/v0/inboxes/{E('AGENTMAIL_ADDRESS')}/messages?limit=3 with header 'Authorization: Bearer {E('AGENTMAIL_API_KEY')}' — check subject/preview fields"


def browser_subagent(task: str, url: str | None = None) -> dict:
    settings = {"profileId": E("BROWSER_USE_PROFILE_ID")}
    if E("PROXY_HOST"):
        settings["customProxy"] = {"host": E("PROXY_HOST"), "port": int(os.environ["PROXY_PORT"]),
                                    "username": E("PROXY_USER"), "password": E("PROXY_PASS")}
    else:
        settings["proxyCountryCode"] = "us"

    body = {"task": task + SKILLS, "sessionSettings": settings}
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
