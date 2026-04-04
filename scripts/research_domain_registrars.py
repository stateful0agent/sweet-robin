import os
import sys
from functions.browser_use import browser_subagent


def main():
    task = """
    Research domain registrars that have a high success rate with US-issued prepaid Visa cards (like Vanilla Gift).
    Specifically check:
    1. Dynadot: Does it enforce AVS or 3D Secure strictly? Can I top up balance with a prepaid card?
    2. Sav.com: Does it allow PayPal guest payments for balance top-up or direct checkout?
    3. Epik: What is their current reputation and payment flexibility?
    4. European registrars: Are there any (e.g., Njalla, OrangeWebsite, Infomaniak, OVH, Gandi) that are more lenient with prepaid cards or don't use AVS?
    5. Find if any of these allow 'topping up' account balance via a one-time PayPal guest payment.
    
    Summarize the findings for each and recommend the best option for buying 'autonomousrobin.news'.
    """

    print("Starting browser research task...")
    result = browser_subagent(task)

    if result.get("status") == "finished":
        print("\nResearch Findings:")
        print(result.get("output", "No output returned"))

        # Save results to a file for later reference
        with open("journal/domain_research_2026-04-04.md", "w") as f:
            f.write("# Domain Registrar Research - 2026-04-04\n\n")
            f.write(result.get("output", "No output returned"))
    else:
        print(f"\nTask failed with status: {result.get('status')}")
        print(f"Error: {result.get('output', 'Unknown error')}")


if __name__ == "__main__":
    main()
