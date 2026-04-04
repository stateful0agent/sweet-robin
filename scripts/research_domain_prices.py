import sys
import os
from functions.browser_use import browser_subagent


def research_domain_prices(domain):
    task = f"""
    Research the first-year price for the domain '{domain}' on the following registrars:
    1. Porkbun
    2. Namecheap
    3. NameSilo
    4. Sav.com

    For each registrar, find:
    - The first-year registration price.
    - Any additional taxes or fees (like the $0.18 ICANN fee).
    - If there is a current sale on the .news TLD.
    - The total price for the first year.

    Return the results in a clear format.
    """

    print(f"Starting research for {domain}...")
    result = browser_subagent(task)

    if result.get("status") == "finished":
        print("Research finished successfully.")
        print("Output:")
        print(result.get("output"))
    else:
        print(f"Research failed with status: {result.get('status')}")
        print("Error/Output:")
        print(result.get("output"))


if __name__ == "__main__":
    domain = "autonomousrobin.news"
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    research_domain_prices(domain)
