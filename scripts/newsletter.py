import json
import os
import sys
import requests
import time
from datetime import datetime, timedelta
from functions.browser_use import browser_subagent


def get_hacker_news_top_stories(limit=3):  # Reduced limit for testing
    # Use Algolia API for better filtering
    one_day_ago = int((datetime.now() - timedelta(days=1)).timestamp())
    url = f"https://hn.algolia.com/api/v1/search?tags=story&numericFilters=created_at_i>{one_day_ago},points>100&hitsPerPage={limit}"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    stories = []
    for hit in data.get("hits", []):
        stories.append(
            {
                "title": hit["title"],
                "url": hit["url"]
                or f"https://news.ycombinator.com/item?id={hit['objectID']}",
                "points": hit["points"],
                "author": hit["author"],
                "num_comments": hit["num_comments"],
            }
        )
    return stories


def summarize_stories(stories):
    print("Summarizing stories using browser sub-agent...")
    summary_request = "Summarize each of the following news stories in a single sentence. Output only the summaries as a numbered list:\n\n"
    for i, story in enumerate(stories, 1):
        summary_request += f"{i}. {story['title']} - {story['url']}\n"

    result = browser_subagent(summary_request)
    return result.get("output", "Summary unavailable.")


from scripts.send_mail import send


def main():
    print(f"Fetching top Hacker News stories...")
    stories = get_hacker_news_top_stories(limit=3)

    if not stories:
        print("No top stories found.")
        return

    print(f"Found {len(stories)} stories.")

    summaries = summarize_stories(stories)

    newsletter_content = "# The Autonomous Robin Newsletter\n\n"
    newsletter_content += (
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )
    newsletter_content += "Here are the top stories from Hacker News from the last 24 hours, summarized for you:\n\n"

    newsletter_content += summaries + "\n\n"

    newsletter_content += "---\n\n"
    newsletter_content += "### Detailed Links\n\n"
    for i, story in enumerate(stories, 1):
        newsletter_content += f"{i}. [{story['title']}]({story['url']}) ({story['points']} points by {story['author']} | {story['num_comments']} comments)\n"

    print("\nNewsletter Draft:\n")
    print(newsletter_content)

    # Save the draft
    os.makedirs("newsletters", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"newsletters/{today}.md", "w") as f:
        f.write(newsletter_content)
    print(f"\nSaved draft to newsletters/{today}.md")

    # Load subscribers
    subscribers_file = "subscribers.json"
    if os.path.exists(subscribers_file):
        with open(subscribers_file, "r") as f:
            subscribers = json.load(f)
    else:
        subscribers = ["sweet.robin.163@agentmail.to"]

    # Send to subscribers
    subject = f"The Autonomous Robin Newsletter - {today}"
    for email in subscribers:
        print(f"Sending to {email}...")
        try:
            send(email, subject, newsletter_content)
        except Exception as e:
            print(f"Failed to send to {email}: {e}")


if __name__ == "__main__":
    main()
