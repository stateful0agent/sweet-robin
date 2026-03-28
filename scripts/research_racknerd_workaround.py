import sys, os
from functions.browser_use import browser_subagent


def main():
    task = "Check if RackNerd (clientarea.racknerd.com) allows 'Adding Funds' to an account balance using PayPal as a one-time transaction. This would be a workaround for the Vanilla Visa's failure on direct recurring card payments. Summarize if this is possible and if it works for paying invoices."

    print(f"Task: {task}")
    result = browser_subagent(task)

    if result.get("status") == "finished":
        print("\n--- RESULTS ---")
        print(result.get("output"))

        with open("journal/racknerd_workaround_research.md", "a") as f:
            f.write(
                f"\n\n# RackNerd Payment Workaround - 2026-03-28\n\n{result.get('output')}"
            )
    else:
        print(f"Task status: {result.get('status')}")
        print(f"Output: {result.get('output')}")


if __name__ == "__main__":
    main()
