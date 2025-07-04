# DiscoRSS

<img src="https://wakapi-qt1b.onrender.com/api/badge/fahad/interval:any/project:DiscoRSS" 
     alt="Wakapi Time Tracking" 
     title="Spent more than that amount of time spent on this project">

This Python script fetches the latest entries from multiple RSS feeds and sends them to a Discord channel. The bot uses the discord and feedparser libraries to interact with Discord and parse RSS feeds, respectively.

# Dependencies

* discord
* feedparser
* dotenv
* pyyaml

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

1. Store the Discord Channel ID, Bot Token, RSS Feed URLs and Timezone to `.env` under the `DISCORD_CHANNEL_ID`, `DISCORD_BOT_TOKEN`, and `RSS_FEED_URLS`

[![image.png](https://i.postimg.cc/kGgV2CkH/image.png)](https://postimg.cc/njNVWyVK)

You're all set.

## Run the bot on the desktop

1. Open a terminal or command prompt

2. Navigate to the directory where you cloned the repository

3. Run `python3 main.py` to start the bot

## How the bot works

* This bot works by periodically fetching the latest articles from one or more RSS feeds and sending them to specified Discord channels.

* When the bot starts, it logs in to Discord using a bot token and sets up a loop that runs indefinitely. Inside the loop, the bot fetches the RSS feeds and checks for new articles. If a new article is found, the bot sends a message to the specified Discord channel with the article title and link.

* The bot keeps track of which articles have already been sent to each channel using a YAML file called sent_articles.yaml. This file is updated every time a new article is sent, to ensure that duplicate articles are not sent to the same channel.
