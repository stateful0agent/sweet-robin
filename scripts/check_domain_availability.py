import os
import requests

API = "https://api.browser-use.com/api/v2"
HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}
E = os.environ.get


def main():
    task = "Check if 'autonomousrobin.news' is registered and who the registrant is if possible. Just tell me if it is registered or not."
    settings = {"profileId": E("BROWSER_USE_PROFILE_ID")}
    body = {
        "task": task,
        "sessionSettings": settings,
        "startUrl": "https://www.whois.com/whois/autonomousrobin.news",
    }

    resp = requests.post(f"{API}/tasks", json=body, headers=HDR)
    if resp.status_code in (201, 202):
        tid = resp.json()["id"]
        print(f"Check task {tid} started.")
    else:
        print(f"Failed: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    main()
