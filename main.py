import discord
import feedparser
import os
from dotenv import load_dotenv
import yaml
import asyncio

load_dotenv()
intents = discord.Intents.all()
client = discord.Client(intents=intents)
# Information needed for discord authentication
DISCORD_CHANNEL_IDS = list(map(int, os.getenv('DISCORD_CHANNEL_IDS').split(',')))
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
RSS_FEED_URLS = os.getenv('RSS_FEED_URLS').split(",")
EMOJI = "\U0001F4F0"  # Newspaper emoji
sent_articles_file = "sent_articles.yaml"

async def fetch_feed(channel):
    # Load the seen IDs from the file, or create an empty dictionary
    if os.path.exists(sent_articles_file):
        with open(sent_articles_file, "r") as f:
            sent_articles = yaml.safe_load(f)
        print("Loaded YAML object")
    else:
        sent_articles = {}
        print("Created new empty dictionary")

    for rss_feed_url in RSS_FEED_URLS:
        # Parse the RSS feed
        print("Parsing RSS feed...")
        feed = feedparser.parse(rss_feed_url)

        # Check if the feed was parsed successfully
        if feed.bozo:
            print(f"Error parsing RSS feed: {feed.bozo_exception}")
            continue

        last_entry = feed.entries[0]
        if channel.id not in sent_articles:
            sent_articles[channel.id] = []
        if last_entry.link not in sent_articles[channel.id]:
            article_title = last_entry.title
            article_link = last_entry.link
            sent_articles[channel.id].append(last_entry.link)

            print(f"New article: {article_title}")
            print(f"Link: {article_link}")

            try:
                # Send the article link to the channel
                await channel.send(f"{EMOJI}  |  {article_title}\n\n{article_link}")
                print("Article sent to channel successfully")
            except discord.Forbidden:
                print("Error: Insufficient permissions to send messages to the channel")
            except discord.HTTPException as e:
                print(f"Error sending message to the channel: {e}")

        print(f"Parsing complete for {rss_feed_url}")

    while True:
        try:
            with open(sent_articles_file, "w") as f:
                yaml.dump(sent_articles, f, default_flow_style=False, sort_keys=False)
            break  # Exit the loop if the file was written successfully
        except Exception as e:
            print(f"Error writing seen IDs to file: {e}")
            await asyncio.sleep(1)  # Wait for 1 second before trying again
    
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user.name}")

    while True:
        for channel_id in DISCORD_CHANNEL_IDS:
            # Get the desired channel object
            channel = client.get_channel(channel_id)
            print(f"Target channel: {channel.name} (ID: {channel.id})")
            # Fetch the RSS feed
            await fetch_feed(channel)

        await asyncio.sleep(600) # Wait for 60 seconds before fetching again

# Start the bot
print("Starting the bot...")
client.run(DISCORD_BOT_TOKEN)
