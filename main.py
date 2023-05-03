import discord
import feedparser
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Information needed for discord authentication
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TIMEZONE = os.getenv('TIMEZONE')

RSS_FEED_URLS = os.getenv('RSS_FEED_URLS').split(",")
EMOJI = "\U0001F4F0"  # Newspaper emoji
LATEST_ENTRIES_FILE = "latest_entries.json"

# Load the latest entries from the file
try:
    with open(LATEST_ENTRIES_FILE) as f:
        latest_entries = json.load(f)
except FileNotFoundError:
    latest_entries = {}

async def send_latest_entries():
    for rss_feed_url in RSS_FEED_URLS:
        # Fetch the RSS feed
        feed = feedparser.parse(rss_feed_url)
          
        # Send the latest entry to the channel if it's not in the latest_entries dict
        latest_entry = feed.entries[0]
        title = latest_entry.title
        link = latest_entry.link
        if rss_feed_url not in latest_entries or latest_entries[rss_feed_url] != link:
            message = f"{EMOJI}  |  {title}\n\n{link}"
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            await channel.send(message)
            latest_entries[rss_feed_url] = link

    # Save the latest entries to the file with indentation
    with open(LATEST_ENTRIES_FILE, "w") as f:
        json.dump(latest_entries, f, indent=4)


intents = discord.Intents.all()
client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler(timezone=TIMEZONE)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

    # Schedule the send_latest_entries function to run every 5 minutes
    scheduler.add_job(send_latest_entries, "interval", minutes=5)
    scheduler.start()

client.run(DISCORD_BOT_TOKEN)