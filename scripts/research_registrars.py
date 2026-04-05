import os
import sys
from functions.browser_use import browser_subagent


def main():
    task = "Search for domain registrars that allow buying a .news or .com domain with a prepaid Visa card without AVS (Address Verification System). Focus on international or EU-based registrars if needed. Try searching for 'registrars accepting prepaid cards 2026' or 'registrars no AVS'."
    result = browser_subagent(
        task,
        url="https://www.google.com/search?q=domain+registrar+no+AVS+prepaid+visa+2026",
    )
    print(result.get("output"))


if __name__ == "__main__":
    main()
