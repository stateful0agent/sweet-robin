import sys, os
from functions.browser_use import browser_subagent


def main():
    task = "Find a domain registrar or VPS provider that is known to work with Vanilla Visa Gift cards. Vanilla cards often fail on Stripe due to lack of 3D Secure or strict AVS. Look for providers that use different payment gateways (e.g., BitPay, CoinGate, or manual PayPal) or have documented success with prepaid cards. Check Dynadot, Sav.com, Porkbun, or Namecheap. Also check if any of them accept PayPal and if I can use the Vanilla card on PayPal for these services. Summarize the best options and any known workarounds."

    print(f"Task: {task}")
    result = browser_subagent(task)

    if result.get("status") == "finished":
        print("\n--- RESULTS ---")
        print(result.get("output"))

        with open("journal/payment_research_vanilla.md", "w") as f:
            f.write(
                f"# Payment Research Results - Vanilla Visa - 2026-03-28\n\n{result.get('output')}"
            )
    else:
        print(f"Task status: {result.get('status')}")
        print(f"Output: {result.get('output')}")


if __name__ == "__main__":
    main()
