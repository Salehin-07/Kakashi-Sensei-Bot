import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import aiohttp
from datetime import datetime
from flask import Flask

# Flask setup
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1> Bot is running </h1>"

# Load .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='&', intents=intents)

# Globals
check_task = None
last_seen_titles = set()
notification_channel = None

# Helper
def get_channel_display(channel):
    return "📩 Direct Message" if isinstance(channel, discord.DMChannel) else channel.mention

# Anime fetcher
async def fetch_recent_episodes():
    global last_seen_titles, notification_channel

    apis = [
        {"name": "Current Season", "url": "https://api.jikan.moe/v4/seasons/now", "key": "data"},
        {"name": "Currently Airing", "url": "https://api.jikan.moe/v4/top/anime?filter=airing&limit=25", "key": "data"}
    ]

    async with aiohttp.ClientSession() as session:
        new_episodes = []

        for api in apis:
            try:
                async with session.get(api['url'], timeout=15) as res:
                    if res.status != 200:
                        continue

                    data = await res.json()
                    anime_list = data.get(api['key'], [])
                    for anime in anime_list[:10]:
                        title = anime.get('title', 'Unknown')
                        title_english = anime.get('title_english') or title
                        mal_id = anime.get('mal_id')
                        unique_id = f"{mal_id}_{title}"

                        if unique_id not in last_seen_titles:
                            new_episodes.append({
                                'title': title_english,
                                'title_jp': title,
                                'mal_id': mal_id,
                                'score': anime.get('score'),
                                'status': anime.get('status'),
                                'aired_from': anime.get('aired', {}).get('from'),
                                'episodes': anime.get('episodes'),
                                'url': anime.get('url'),
                                'image': anime.get('images', {}).get('jpg', {}).get('image_url', ''),
                                'synopsis': anime.get('synopsis', '')[:200] + '...' if anime.get('synopsis') else 'No synopsis available'
                            })
                            last_seen_titles.add(unique_id)

                await asyncio.sleep(1)

            except:
                continue

        if new_episodes and notification_channel:
            embed = discord.Embed(
                title="🎉 New Anime Updates!",
                color=0x00ff00,
                description="Recently updated anime from MyAnimeList",
                timestamp=datetime.utcnow()
            )

            for anime in new_episodes[:5]:
                value = f"**Status:** {anime['status']}\n"
                if anime['score']:
                    value += f"**Score:** {anime['score']}/10\n"
                if anime['episodes']:
                    value += f"**Episodes:** {anime['episodes']}\n"
                value += f"**Synopsis:** {anime['synopsis']}\n"
                value += f"[View on MAL]({anime['url']})"
                embed.add_field(name=f"📺 {anime['title']}", value=value, inline=False)

            if len(new_episodes) > 5:
                embed.add_field(name="And more...", value=f"{len(new_episodes) - 5} additional anime updates!", inline=False)

            embed.set_footer(text="Powered by Jikan API (MyAnimeList)")

            if new_episodes[0]['image']:
                embed.set_thumbnail(url=new_episodes[0]['image'])

            await notification_channel.send(embed=embed)

# Check loop
async def check_loop():
    await fetch_recent_episodes()
    while True:
        try:
            await asyncio.sleep(3600)
            await fetch_recent_episodes()
        except asyncio.CancelledError:
            break
        except:
            await asyncio.sleep(600)

# Events
@client.event
async def on_ready():
    print(f'✅ {client.user} is online!')
    print(f'📊 Connected to {len(client.guilds)} server(s)')

# Commands
@client.command()
async def start(ctx):
    global check_task, notification_channel
    if check_task and not check_task.done():
        await ctx.send("❌ Anime checker is already running!")
        return

    notification_channel = ctx.channel
    check_task = asyncio.create_task(check_loop())

    embed = discord.Embed(
        title="✅ Anime Checker Started!",
        description="Using Jikan API (MyAnimeList) for reliable anime updates",
        color=0x00ff00
    )
    embed.add_field(name="📍 Channel Set", value=get_channel_display(ctx.channel), inline=False)
    embed.add_field(name="⏰ Check Interval", value="Every 60 minutes (respects API rate limits)", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def stop(ctx):
    global check_task
    if check_task and not check_task.done():
        check_task.cancel()
        try:
            await check_task
        except asyncio.CancelledError:
            pass
        await ctx.send("🛑 Anime release checker stopped.")
    else:
        await ctx.send("❌ Anime checker is not running!")

@client.command()
async def status(ctx):
    global check_task, notification_channel
    embed = discord.Embed(title="📊 Bot Status", color=0x0099ff)

    embed.add_field(name="🟢 Checker Status" if check_task and not check_task.done() else "🔴 Checker Status",
                    value="Running" if check_task and not check_task.done() else "Stopped",
                    inline=True)

    embed.add_field(name="📍 Notification Channel",
                    value=get_channel_display(notification_channel) if notification_channel else "Not set",
                    inline=True)

    embed.add_field(name="📈 Anime Tracked", value=len(last_seen_titles), inline=True)
    embed.add_field(name="🌐 API Source", value="Jikan (MyAnimeList)", inline=True)

    await ctx.send(embed=embed)

@client.command()
async def setchannel(ctx):
    global notification_channel
    notification_channel = ctx.channel
    await ctx.send(embed=discord.Embed(
        title="✅ Channel Updated!",
        description=f"Notifications will now be sent to {get_channel_display(ctx.channel)}",
        color=0x00ff00
    ))

@client.command()
async def test(ctx):
    await ctx.send("🔍 Testing API connection...")
    await fetch_recent_episodes()
    await ctx.send("✅ Test completed! Check console for results.")

@client.command()
async def clear(ctx):
    global last_seen_titles
    count = len(last_seen_titles)
    last_seen_titles.clear()
    await ctx.send(f"🗑️ Cleared {count} tracked anime from cache.")

@client.command()
async def hello(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("👋 Hello! You're messaging me in DMs.")
    else:
        await ctx.send("👋 Hello from the server!")

# Error handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Unknown command! Use `&help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing arguments! Check the command usage.")
    else:
        print(f"Error: {error}")
        await ctx.send("❌ Something went wrong while processing the command.")

# Run
if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

    if not TOKEN:
        print("❌ Discord token not found! Set DISCORD_TOKEN in .env")
    else:
        client.run(TOKEN)