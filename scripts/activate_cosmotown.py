import sys, os

sys.path.append(os.getcwd())
from functions.browser_use import browser_subagent


def main():
    url = "https://www.cosmotown.com/main/activateAccount/activate/128615273369d3680e70bee"
    task = "Set a strong password 'RobinAgent2026!' in the password and confirm password fields, then click the button to complete account activation."
    result = browser_subagent(task, url=url)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
