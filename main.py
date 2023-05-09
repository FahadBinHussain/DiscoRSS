import discord
import feedparser
import os
from dotenv import load_dotenv
import asyncio
import datetime
import json

load_dotenv()

# Information needed for discord authentication
DISCORD_CHANNEL_IDS = list(map(int, os.getenv('DISCORD_CHANNEL_IDS').split(',')))
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TIMEZONE = os.getenv('TIMEZONE')

RSS_FEED_URLS = os.getenv('RSS_FEED_URLS').split(",")
EMOJI = "\U0001F4F0"  # Newspaper emoji

# Load the last_checked dictionary from a JSON file, if it exists
if os.path.exists('last_checked.json'):
    with open('last_checked.json', 'r') as f:
        last_checked = {url: datetime.datetime.fromisoformat(last_checked_str) for url, last_checked_str in json.load(f).items()}
else:
    # Create a new dictionary if the JSON file does not exist
    last_checked = {rss_feed_url: datetime.datetime.now() for rss_feed_url in RSS_FEED_URLS}

async def send_latest_entries():
    while True:
        for rss_feed_url in RSS_FEED_URLS:
            # Fetch the RSS feed
            feed = feedparser.parse(rss_feed_url)

            # Wait for 5 seconds before processing the feed
            await asyncio.sleep(5)

            # Send new entries to the channels that were published after the last check
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                published_time = datetime.datetime(*entry.published_parsed[:6])
                if published_time > last_checked[rss_feed_url]:
                    message = f"{EMOJI}  |  {title}\n\n{link}"
                    for channel_id in DISCORD_CHANNEL_IDS:
                        channel = client.get_channel(channel_id)
                        await channel.send(message)
                    last_checked[rss_feed_url] = published_time
                    print(f"Sent {link} to Discord")
                else:
                    break

        # Save the last_checked dictionary as a JSON file
        with open('last_checked.json', 'w') as f:
            json.dump({url: last_checked_str.isoformat() for url, last_checked_str in last_checked.items()}, f)

        # Wait for 5 minutes before checking for new articles again
        await asyncio.sleep(300)


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

    # Start the send_latest_entries function in a loop
    asyncio.create_task(send_latest_entries())

client.run(DISCORD_BOT_TOKEN)
