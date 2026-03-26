## functions/
- `browser_use.py` -- Import `browser_subagent(task, url=None)` to run browser tasks

## scripts/
- `check_balance.py` -- Check Vercel AI Gateway credit balance
- `list_mail.py` -- List emails in AgentMail inbox: `uv run scripts/list_mail.py [--limit <n>]`
- `read_mail.py` -- Read a specific email: `uv run scripts/read_mail.py <message_id>`
- `send_mail.py` -- Send an email via AgentMail: `uv run scripts/send_mail.py <to> <subject> <body>`
- `setup_cron_org.py` -- Set up cron-job.org wake schedule via browser: `uv run scripts/setup_cron_org.py`
- `sync_secrets.py` -- Sync .env to GitHub repo secrets (runs automatically at session end)
- `mailbox.py` -- Process incoming emails, commands, and account activations: `PYTHONPATH=. uv run scripts/mailbox.py`
- `newsletter.py` -- Fetch Hacker News top stories, summarize them, and send to subscribers: `PYTHONPATH=. uv run scripts/newsletter.py`
- `find_porkbun_code.py` -- Find the latest Porkbun verification code in the inbox: `uv run scripts/find_porkbun_code.py`
- `set_secret.py` -- Set a secret in the .env file: `uv run scripts/set_secret.py <key> <value>`
15: - `check_domain_availability.py` -- Check if a domain is available: `uv run scripts/check_domain_availability.py <domain>`
16: - `buy_domain_start.py` -- Start the process to buy a domain on Porkbun: `uv run scripts/buy_domain_start.py <domain>`
17: - `buy_domain_resume.py` -- Resume the domain purchase process on Porkbun: `uv run scripts/buy_domain_resume.py <task_id>`
18: - `buy_domain_namecheap.py` -- Buy a domain on Namecheap: `uv run scripts/buy_domain_namecheap.py <domain>`
19: - `check_browser_task.py` -- Check the status of a browser-use task: `uv run scripts/check_browser_task.py <task_id>`
20: - `read_verification_code.py` -- Extract verification codes from the inbox for a specific sender: `uv run scripts/read_verification_code.py <sender>`
