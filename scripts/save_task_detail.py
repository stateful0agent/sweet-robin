import os, sys, requests, json

API = "https://api.browser-use.com/api/v2"
HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}


def save_task_detail(tid):
    resp = requests.get(f"{API}/tasks/{tid}", headers=HDR)
    if resp.status_code == 200:
        detail = resp.json()
        os.makedirs("browser-use-traces", exist_ok=True)
        with open(f"browser-use-traces/{tid}.json", "w") as f:
            json.dump(detail, f, indent=2)
        print(f"Saved detail to browser-use-traces/{tid}.json")
    else:
        print(f"Error: {resp.status_code}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        save_task_detail(sys.argv[1])
    else:
        with open("latest_browser_task.txt", "r") as f:
            tid = f.read().strip()
            save_task_detail(tid)
