import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import aiohttp
from datetime import datetime
from flask import Flask, redirect, render_template_string

# Flask setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kakashi Sensei Bot</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(to right, #23272A, #2C2F33);
                color: #FFFFFF;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 960px;
                margin: auto;
                padding: 40px 20px;
            }
            .card {
                background: #2F3136;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.4);
                padding: 30px;
                margin-top: 20px;
            }
            h1 {
                font-size: 2.6em;
                margin-bottom: 0.4em;
                color: #7289DA;
            }
            .btn {
                display: inline-block;
                background: #7289DA;
                color: white;
                padding: 12px 20px;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 600;
                transition: background 0.3s;
                margin-right: 10px;
            }
            .btn:hover {
                background: #5b6eae;
            }
            ul {
                list-style: none;
                padding-left: 0;
            }
            li::before {
                content: "✔️ ";
                margin-right: 8px;
                color: #43B581;
            }
            .footer {
                margin-top: 40px;
                font-size: 0.9em;
                color: #aaa;
                text-align: center;
            }
            @media (max-width: 600px) {
                .btn { display: block; margin: 10px 0; width: 100%; text-align: center; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>Kakashi Sensei Bot</h1>
                <p>Get automatic updates about new anime episodes from MyAnimeList!</p>
                <a href="/invite" class="btn">Invite Bot to Server</a>
                <a href="/terms" class="btn">Terms of Service</a>
                <a href="/privacy" class="btn">Privacy Policy</a>

                <h2 style="margin-top: 30px;">Bot Features</h2>
                <ul>
                    <li>Automatic updates for currently airing anime</li>
                    <li>Beautiful embed notifications in Discord</li>
                    <li>Customizable notification channels</li>
                    <li>Hourly checks for new episodes</li>
                </ul>
            </div>
            <div class="footer">
                <p>© Kakashi Sensei Bot · Powered by <a href="https://myanimelist.net/" style="color: #7289DA;">MyAnimeList</a></p>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/invite')
def invite():
    return redirect("https://discord.com/oauth2/authorize?client_id=1386331041782042735&permissions=0&integration_type=0&scope=bot")

@app.route('/terms')
def terms():
    return render_template_string('''
    <html>
    <head><title>Terms of Service</title></head>
    <body style="font-family: Arial; background: #2c2f33; color: white; padding: 40px; max-width: 800px; margin: auto;">
        <h1 style="color: #7289DA;">Terms of Service</h1>
        <p>Last Updated: June 23, 2025</p>
        <h2>1. Acceptance of Terms</h2>
        <p>By using the bot, you agree to follow these terms.</p>
        <h2>2. Description of Service</h2>
        <p>This bot sends anime episode updates from MyAnimeList using the Jikan API.</p>
        <h2>3. User Responsibilities</h2>
        <p>Don’t use the bot for illegal or abusive purposes.</p>
        <h2>4. Limitation of Liability</h2>
        <p>We’re not liable for damages caused by the bot’s use.</p>
        <h2>5. Changes</h2>
        <p>We can update these terms anytime.</p>
    </body>
    </html>
    ''')

@app.route('/privacy')
def privacy():
    return render_template_string('''
    <html>
    <head><title>Privacy Policy</title></head>
    <body style="font-family: Arial; background: #2c2f33; color: white; padding: 40px; max-width: 800px; margin: auto;">
        <h1 style="color: #7289DA;">Privacy Policy</h1>
        <p>Last Updated: June 24, 2025</p>
        <h2>1. What We Collect</h2>
        <p>Only the Discord channel IDs where updates are sent.</p>
        <h2>2. Why We Collect</h2>
        <p>So we can send updates to your selected channels.</p>
        <h2>3. Storage</h2>
        <p>Data isn’t stored long-term or shared.</p>
        <h2>4. Third-Party</h2>
        <p>We use MyAnimeList’s public API via Jikan.</p>
        <h2>5. Updates</h2>
        <p>We can change this policy anytime.</p>
    </body>
    </html>
    ''')

# Load env and bot setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='?', intents=intents)

# Globals
check_task = None
last_seen_titles = set()
notification_channel = None

def get_channel_display(channel):
    return "📩 Direct Message" if isinstance(channel, discord.DMChannel) else channel.mention
9
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
                    for anime in data.get(api['key'], [])[:10]:
                        title = anime.get('title', 'Unknown')
                        title_en = anime.get('title_english') or title
                        mal_id = anime.get('mal_id')
                        unique_id = f"{mal_id}_{title}"
                        if unique_id not in last_seen_titles:
                            new_episodes.append({
                                'title': title_en,
                                'mal_id': mal_id,
                                'url': anime.get('url'),
                                'image': anime.get('images', {}).get('jpg', {}).get('image_url', ''),
                                'synopsis': anime.get('synopsis', '')[:200] + '...' if anime.get('synopsis') else 'No synopsis available',
                                'status': anime.get('status'),
                                'score': anime.get('score'),
                                'episodes': anime.get('episodes'),
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
                if anime['score']: value += f"**Score:** {anime['score']}/10\n"
                if anime['episodes']: value += f"**Episodes:** {anime['episodes']}\n"
                value += f"**Synopsis:** {anime['synopsis']}\n"
                value += f"[View on MAL]({anime['url']})"
                embed.add_field(name=f"📺 {anime['title']}", value=value, inline=False)
            if len(new_episodes) > 5:
                embed.add_field(name="And more...", value=f"{len(new_episodes) - 5} more updates!", inline=False)
            embed.set_footer(text="Powered by Jikan API (MyAnimeList)")
            if new_episodes[0]['image']:
                embed.set_thumbnail(url=new_episodes[0]['image'])
            await notification_channel.send(embed=embed)

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

@client.event
async def on_ready():
    print(f'✅ {client.user} is online!')
    print(f'📊 Connected to {len(client.guilds)} server(s)')

@client.command()
async def start(ctx):
    global check_task, notification_channel
    if check_task and not check_task.done():
        await ctx.send("❌ Already running!")
        return
    notification_channel = ctx.channel
    check_task = asyncio.create_task(check_loop())
    await ctx.send(embed=discord.Embed(
        title="✅ Started!",
        description=f"Updates will be posted in {get_channel_display(ctx.channel)}",
        color=0x00ff00
    ))

@client.command()
async def stop(ctx):
    global check_task
    if check_task and not check_task.done():
        check_task.cancel()
        try: await check_task
        except asyncio.CancelledError: pass
        await ctx.send("🛑 Stopped!")
    else:
        await ctx.send("❌ Not running!")

@client.command()
async def status(ctx):
    embed = discord.Embed(title="📊 Status", color=0x0099ff)
    embed.add_field(name="Checker", value="🟢 Running" if check_task and not check_task.done() else "🔴 Stopped", inline=True)
    embed.add_field(name="Channel", value=get_channel_display(notification_channel) if notification_channel else "Not set", inline=True)
    embed.add_field(name="Tracked", value=str(len(last_seen_titles)), inline=True)
    embed.add_field(name="Source", value="Jikan (MyAnimeList)", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def setchanel(ctx):
    global notification_channel
    notification_channel = ctx.channel
    await ctx.send(embed=discord.Embed(
        title="✅ Channel Updated!",
        description=f"Now using {get_channel_display(ctx.channel)}",
        color=0x00ff00
    ))

@client.command()
async def clear(ctx):
    count = len(last_seen_titles)
    last_seen_titles.clear()
    await ctx.send(f"🧹 Cleared {count} cached anime.")

@client.command()
async def hello(ctx):
    await ctx.send("👋 Hello! I'm Kakashi Sensei Bot.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Unknown command. Try `?help`.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Missing argument.")
    else:
        await ctx.send("⚠️ Something went wrong.")
        print(error)

# Run app + bot
if __name__ == "__main__":
    if not TOKEN:
        print("❌ Missing token in .env!")
    else:
        client.run(TOKEN)
    
    import threading
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
