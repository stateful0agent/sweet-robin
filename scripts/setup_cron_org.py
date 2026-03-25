"""Set up a cron-job.org job to dispatch GitHub Actions wake events."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from functions.browser_use import browser_subagent

repo = os.environ["GITHUB_REPOSITORY"]
pat = os.environ["REPO_PAT"]
dispatch_url = f"https://api.github.com/repos/{repo}/dispatches"

browser_subagent(f"""Go to https://console.cron-job.org and complete these steps:

1. Sign up for an account with agentmail email and password, arbitrary name
2. Read agentmail email to get email confirmation link and navigate to it
3. Sign into account
4. Create a new cron job with these settings:
   - Title: "AGI Wake"
   - URL: {dispatch_url}
   - Schedule: Custom crontab expression: 0 * * * *
   - Under "Headers", add these key-value pairs:
     - Authorization: token {pat}
     - Accept: application/vnd.github+json
     - Content-Type: application/json
   - Under "Advanced":
     - Change Method dropdown from GET to POST
     - Set Time Zone to America/Los_Angeles
     - Set Request Body to: {{"event_type":"wake"}}
5. Save the job
6. Return the job ID and the account credentials used (email/password)""",
url="https://console.cron-job.org")
