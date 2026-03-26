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


def get_github_trending(limit=3):
    print("Fetching GitHub trending repositories...")
    task = f"Go to https://github.com/trending and list the top {limit} trending repositories (name and link)."
    result = browser_subagent(task, url="https://github.com/trending")
    # Parse output - simple parsing for now
    return result.get("output", "Trending repositories unavailable.")


def summarize_content(hn_stories, github_trending):
    print("Summarizing content using browser sub-agent...")
    content_to_summarize = "Hacker News Stories:\n"
    for i, story in enumerate(hn_stories, 1):
        content_to_summarize += f"{i}. {story['title']} - {story['url']}\n"

    content_to_summarize += "\nGitHub Trending:\n"
    content_to_summarize += github_trending

    summary_request = f"""
    Summarize the following content for a newsletter called 'The Autonomous Robin'.
    For Hacker News, provide a single sentence summary for each story.
    For GitHub Trending, provide a brief summary of what's trending.
    Output the summary in Markdown format.
    """

    result = browser_subagent(summary_request + "\n\nContent:\n" + content_to_summarize)
    return result.get("output", "Summary unavailable.")


from scripts.send_mail import send


def main():
    print(f"Fetching content for today's newsletter...")
    hn_stories = get_hacker_news_top_stories(limit=5)
    github_trending = get_github_trending(limit=3)

    if not hn_stories:
        print("No top HN stories found.")
        return

    summaries = summarize_content(hn_stories, github_trending)

    newsletter_content = "# The Autonomous Robin Newsletter\n\n"
    newsletter_content += (
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )
    newsletter_content += summaries + "\n\n"

    newsletter_content += "---\n\n"
    newsletter_content += "### Hacker News Detailed Links\n\n"
    for i, story in enumerate(hn_stories, 1):
        newsletter_content += f"{i}. [{story['title']}]({story['url']}) ({story['points']} points by {story['author']} | {story['num_comments']} comments)\n"

    newsletter_content += "\n### GitHub Trending Detailed\n\n"
    newsletter_content += github_trending + "\n\n"

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
