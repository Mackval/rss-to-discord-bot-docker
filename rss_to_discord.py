import requests
import time
import os
import json

JSON_FEED_URL = 'https://www.inoreader.com/stream/user/1003782884/tag/Game%20News/view/json'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1356337247955325103/LiXBGdq9OMWT_W5GSSL1mS-LjK7nqP4KHZt0RQrk08w59fKhhJoVHVuOe532VAJMsKu5'
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
    print(f"🔎 Found {len(items)} items in the feed.")
    if not items:
        print("⚠️ No items found in JSON feed.")
        return

    posted_links = get_posted_links()
    new_items = []

    for item in reversed(items):
        title = item.get("title", "No title")

        # More reliable link extraction
        alternates = item.get("alternate", [])
        link = alternates[0].get("href") if alternates else None

       if not link:
    print(f"⚠️ Skipping item (no valid link): {title}")
    print(json.dumps(item, indent=2))
    continue


        print(f"🔗 Processing: {title} - {link}")

        if link not in posted_links:
            new_items.append((title, link))

    if not new_items:
        print("⏳ No new articles to post. Waiting...")
        return

    for title, link in new_items:
        message = f"📰 **{title}**\n{link}"
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

        if response.status_code == 204:
            print(f"✅ Posted: {title}")
            save_posted_link(link)
        else:
            print(f"❌ Failed to post: {title}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")

print("🔄 Bot is running. Checking every 60 seconds...")
while True:
    fetch_and_post()
    time.sleep(60)
