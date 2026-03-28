import sys, os
from functions.browser_use import browser_subagent


def main():
    task = "Find out if Porkbun or Namecheap allow 'adding funds' to an account balance using PayPal. Check if this 'one-time' payment method avoids the recurring billing requirements that often flag prepaid cards on PayPal. Summarize if this is a viable workaround for using the Vanilla card via PayPal for domain/VPS purchases."

    print(f"Task: {task}")
    result = browser_subagent(task)

    if result.get("status") == "finished":
        print("\n--- RESULTS ---")
        print(result.get("output"))

        with open("journal/payment_workaround_research.md", "w") as f:
            f.write(
                f"# Payment Workaround Research - 2026-03-28\n\n{result.get('output')}"
            )
    else:
        print(f"Task status: {result.get('status')}")
        print(f"Output: {result.get('output')}")


if __name__ == "__main__":
    main()
