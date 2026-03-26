import os
import requests
import json

API = "https://api.browser-use.com/api/v2"
HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}


def check_task(tid):
    resp = requests.get(f"{API}/tasks/{tid}", headers=HDR)
    if resp.status_code == 200:
        detail = resp.json()
        print(f"Status: {detail['status']}")
        print(f"Output: {detail.get('output', 'None')}")
        if detail["status"] == "started":
            # Print last step if available
            steps = detail.get("steps", [])
            if steps:
                last_step = steps[-1]
                print(f"Last Step Number: {last_step.get('number')}")
                print(f"Last URL: {last_step.get('url')}")
                print(f"Last Actions: {last_step.get('actions')}")
            else:
                print("No steps yet.")
        return detail
    else:
        print(f"Error: {resp.status_code} {resp.text}")
        return None


if __name__ == "__main__":
    # Get all tasks for the user (if possible)
    # The API might not have a list endpoint, so I'll check common task IDs or I'll just check the last one.
    import sys

    if len(sys.argv) > 1:
        check_task(sys.argv[1])
    else:
        print("Please provide a task ID.")
