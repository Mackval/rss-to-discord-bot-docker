import requests
import time
import os
import json

JSON_FEED_URL = 'https://www.inoreader.com/stream/user/1003782884/tag/Game%20News/view/json'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/your-webhook'
POSTED_LINKS_FILE = 'posted_links.txt'

def get_posted_links():
    if os.path.exists(POSTED_LINKS_FILE):
        with open(POSTED_LINKS_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_posted_link(link):
    with open(POSTED_LINKS_FILE, 'a') as f:
        f.write(link + '\n')

def fetch_and_post():
    try:
        response = requests.get(JSON_FEED_URL)
        data = response.json()
    except Exception as e:
        print("❌ Failed to fetch or parse JSON:", e)
        return

    items = data.get("items", [])
    if not items:
        print("⚠️ No items found in JSON feed.")
        return

    posted_links = get_posted_links()
    new_items = []

    # Loop from oldest to newest
    for item in reversed(items):
        title = item.get("title", "No title")
        link = item.get("alternate", [{}])[0].get("href", "No link")

        if link not in posted_links:
            new_items.append((title, link))

    if not new_items:
        print("⏳ No new articles. Waiting...")
        return

    for title, link in new_items:
        message = f"📰 **{title}**\n{link}"
        post = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

        if post.status_code == 204:
            print(f"✅ Posted: {title}")
            save_posted_link(link)
        else:
            print(f"❌ Failed to post: {title}")
            print(post.text)

print("🔄 Bot is running. Checking every 60 seconds...")
while True:
    fetch_and_post()
    time.sleep(60)
