import os
import sys
from functions.browser_use import browser_subagent


def main():
    task = """
    1. Visit https://www.sav.com and find information about their accepted payment methods.
       Specifically, do they accept prepaid Visa gift cards? Do they allow account balance top-up via PayPal guest payment?
    2. Visit https://www.epik.com and find information about their accepted payment methods.
       Specifically, do they accept prepaid Visa gift cards? Do they allow account balance top-up via PayPal guest payment?
    3. Visit https://njal.la and check if they accept prepaid cards (not just crypto).
    4. Visit https://www.orangewebsite.com and check if they accept prepaid cards.
    
    Summarize which ones are best for a US-issued Vanilla Visa Gift card.
    """

    print("Starting targeted browser research...")
    result = browser_subagent(task)

    if result.get("status") == "finished":
        print("\nResearch Findings:")
        print(result.get("output", "No output returned"))
    else:
        print(f"\nTask failed with status: {result.get('status')}")
        print(f"Error: {result.get('output', 'Unknown error')}")


if __name__ == "__main__":
    main()
