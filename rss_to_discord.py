import requests
import xml.etree.ElementTree as ET
import time
import os

RSS_FEED_URL = 'https://www.inoreader.com/stream/user/1003782884/tag/Game%20News'
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
    response = requests.get(RSS_FEED_URL)
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print("❌ XML parsing error:", e)
        return

    items = list(root.iter('item'))
    if not items:
        print("⚠️ No items found in RSS feed.")
        return

    posted_links = get_posted_links()
    new_items = []

    # Loop through items in reverse (oldest to newest)
    for item in reversed(items):
        title = item.find('title').text if item.find('title') is not None else 'No title'
        link = item.find('link').text if item.find('link') is not None else 'No link'

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

# 🔁 Loop
print("🔄 Bot is running. Checking every 60 seconds...")
while True:
    fetch_and_post()
    time.sleep(60)
