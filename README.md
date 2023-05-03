# DiscoRSS

This Python script fetches the latest entries from multiple RSS feeds and sends them to a Discord channel. The bot uses the discord and feedparser libraries to interact with Discord and parse RSS feeds, respectively.

# Dependencies

* discord
* feedparser
* apscheduler

# How to Use

## Critical prerequisites to install

* run ```pip3 install -r requirements.txt```

* **Rename the file `.env.dev` to `.env`**

## Step 1: Create a Discord bot

1. Go to https://discord.com/developers/applications create an application

[![image-17.png](https://i.postimg.cc/rp6J7h8D/image-17.png)](https://postimg.cc/QFb1TJKD)

2. Build a Discord bot under the application

[![image.png](https://i.postimg.cc/zv5J5JDz/image.png)](https://postimg.cc/TL78JvWF)

3. Click Reset Token and then copy the token

[![image.png](https://i.postimg.cc/sgBCkBPP/image.png)](https://postimg.cc/18Zd63j4)

4. Turn ALL INTENT `ON`

[![image.png](https://i.postimg.cc/RF48ZqtD/image.png)](https://postimg.cc/3yf9L8nX)

5. Invite your bot to your server via OAuth2 URL Generator

[![image.png](https://i.postimg.cc/yd3PBHQb/image.png)](https://postimg.cc/ZBZ3F1h8)

## Step 2: Storing the values

1. Store the Discord Channel ID, Bot Token, RSS Feed URLs and Timezone to `.env` under the `DISCORD_CHANNEL_ID`, `DISCORD_BOT_TOKEN`, `RSS_FEED_URLS` and `TIMEZONE`

[![image.png](https://i.postimg.cc/q7FvKMSB/image.png)](https://postimg.cc/Mcyw2xzg)

2. You're all set.

## Run the bot on the desktop

1. Open a terminal or command prompt

2. Navigate to the directory where you cloned the repository

3. Run `python3 main.py` to start the bot

## Notes

* The script loads the latest entries from the latest_entries.json file and checks if each entry in the RSS feed has already been sent to the Discord channel. If not, it sends the latest entry and updates the latest_entries.json file with the new entry.

* The script uses the apscheduler library to schedule the send_latest_entries function to run every 5 minutes.