import sys, os
from functions.browser_use import browser_subagent


def main():
    task = "Find a domain registrar and VPS provider that accepts Vanilla Visa Gift cards *directly* (without PayPal if possible) or via a gateway that doesn't enforce 3D Secure/AVS strictly. Check if Dynadot or Sav.com use Stripe. Also check if there are VPS providers like BuyVM, RackNerd, or RamNode that have success stories with prepaid cards. Specifically check if Porkbun has an alternative gateway like Apple Pay or Google Pay that might work better for Vanilla cards. Summarize which ones allow direct payment."

    print(f"Task: {task}")
    result = browser_subagent(task)

    if result.get("status") == "finished":
        print("\n--- RESULTS ---")
        print(result.get("output"))

        with open("journal/payment_research_vanilla_direct.md", "w") as f:
            f.write(
                f"# Payment Research Results - Vanilla Visa Direct - 2026-03-28\n\n{result.get('output')}"
            )
    else:
        print(f"Task status: {result.get('status')}")
        print(f"Output: {result.get('output')}")


if __name__ == "__main__":
    main()
