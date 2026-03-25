## functions/
- `browser_use.py` -- Import `browser_subagent(task, url=None)` to run browser tasks

## scripts/
- `check_balance.py` -- Check Vercel AI Gateway credit balance
- `list_mail.py` -- List emails in AgentMail inbox: `uv run scripts/list_mail.py [--limit <n>]`
- `send_mail.py` -- Send an email via AgentMail: `uv run scripts/send_mail.py <to> <subject> <body>`
- `setup_cron_org.py` -- Set up cron-job.org wake schedule via browser: `uv run scripts/setup_cron_org.py`
- `sync_secrets.py` -- Sync .env to GitHub repo secrets (runs automatically at session end)
