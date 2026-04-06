import os, sys, requests, json

API = "https://api.browser-use.com/api/v2"
HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}


def check_task(tid):
    resp = requests.get(f"{API}/tasks/{tid}", headers=HDR)
    if resp.status_code == 200:
        detail = resp.json()
        print(f"Status: {detail['status']}")
        print(f"Output: {detail.get('output', 'None')}")
        steps = detail.get("steps", [])
        if steps:
            for i, step in enumerate(steps[-3:]):
                print(f"Step {step.get('number', i)} URL: {step.get('url')}")
                print(f"Step {step.get('number', i)} Action: {step.get('actions')}")
                if step.get("error"):
                    print(f"Step {step.get('number', i)} Error: {step.get('error')}")

        return detail
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_task(sys.argv[1])
    else:
        with open("latest_browser_task.txt", "r") as f:
            tid = f.read().strip()
            check_task(tid)
