from typing import Any
import json, os, time, requests

API = "https://api.browser-use.com/api/v2"
HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}
E = os.environ.get

SKILLS = ""
if E("AGENTMAIL_ADDRESS") and E("AGENTMAIL_PASSWORD"):
    SKILLS += f"\nFor site logins: prefer Google SSO (profile is logged in). Fallback: email {E('AGENTMAIL_ADDRESS')} password {E('AGENTMAIL_PASSWORD')}"
if E("AGENTMAIL_ADDRESS") and E("AGENTMAIL_API_KEY"):
    SKILLS += f"\nFor email verification codes: GET https://api.agentmail.to/v0/inboxes/{E('AGENTMAIL_ADDRESS')}/messages?limit=3 with header 'Authorization: Bearer {E('AGENTMAIL_API_KEY')}' — check subject/preview fields"


def browser_subagent(task: str, url: str | None = None, retries: int = 1) -> dict:
    for attempt in range(retries + 1):
        try:
            settings: dict[str, Any] = {"profileId": E("BROWSER_USE_PROFILE_ID")}
            if (
                E("PROXY_HOST") and E("PROXY_PORT") and attempt == 0
            ):  # Try with proxy first, then without on retry
                settings["customProxy"] = {
                    "host": E("PROXY_HOST"),
                    "port": int(os.environ["PROXY_PORT"]),
                    "username": E("PROXY_USER"),
                    "password": E("PROXY_PASS"),
                }
            else:
                settings["proxyCountryCode"] = "us"

            body = {"task": task + SKILLS, "sessionSettings": settings}
            if url:
                body["startUrl"] = url

            tid_resp = requests.post(f"{API}/tasks", json=body, headers=HDR)
            tid_resp.raise_for_status()
            tid = tid_resp.json()["id"]
            with open("latest_browser_task.txt", "w") as f:
                f.write(tid)
            print(f"Task {tid} started (attempt {attempt + 1})")

            while True:
                time.sleep(10)  # Polling interval
                resp = requests.get(f"{API}/tasks/{tid}/status", headers=HDR)
                if resp.status_code == 200:
                    status = resp.json()["status"]
                    if status in ("finished", "stopped"):
                        break
                else:
                    print(f"Error checking status: {resp.status_code}")

            detail = requests.get(f"{API}/tasks/{tid}", headers=HDR).json()
            if detail.get("status") == "finished" or attempt == retries:
                os.makedirs("browser-use-traces", exist_ok=True)
                json.dump(detail, open(f"browser-use-traces/{tid}.json", "w"), indent=2)
                print(f"{detail['status']} | {detail.get('output', 'None')}")
                return detail
            else:
                print(f"Task failed with status {detail.get('status')}. Retrying...")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries:
                return {"status": "error", "output": str(e)}
    return {"status": "error", "output": "Max retries reached"}
