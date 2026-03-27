import sys, os
from functions.browser_use import browser_subagent


def main():
    task = "Search for 'best low cost VPS 2026', 'Racknerd annual deals 2026', 'Hetzner cheapest VPS'. Summarize best options <$25/yr for Ubuntu/Docker, payable with prepaid Visa."

    print(f"Task: {task}")
    result = browser_subagent(task)

    if result.get("status") == "finished":
        print("\n--- RESULTS ---")
        print(result.get("output"))

        with open("journal/vps_research.md", "w") as f:
            f.write(f"# VPS Research Results - 2026-03-27\n\n{result.get('output')}")
    else:
        print(f"Task status: {result.get('status')}")
        print(f"Output: {result.get('output')}")


if __name__ == "__main__":
    main()
