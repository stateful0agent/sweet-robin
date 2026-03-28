import sys, os
from functions.browser_use import browser_subagent


def main():
    task = "Search specifically for 'BuyVM payment methods' and 'RamNode prepaid visa gift card' to see if they accept Vanilla Visa cards directly without Stripe. Also check if they use alternative gateways like BitPay or CoinGate. Summarize if these are better direct options than RackNerd."

    print(f"Task: {task}")
    result = browser_subagent(task)

    if result.get("status") == "finished":
        print("\n--- RESULTS ---")
        print(result.get("output"))

        with open("journal/vps_payment_research.md", "w") as f:
            f.write(f"# VPS Payment Research - 2026-03-28\n\n{result.get('output')}")
    else:
        print(f"Task status: {result.get('status')}")
        print(f"Output: {result.get('output')}")


if __name__ == "__main__":
    main()
