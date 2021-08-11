# main.py
import os
import sys

import discord
from dotenv import load_dotenv
import logging
import time
import ast
import re
import random

# prepare logger and log file
log_name = './log/' + time.strftime('%Y-%m-%d_%Hh%Mm%Ss') + '_discord.log'
err_name = log_name + 'err'
sys.stderr = open(err_name, 'w')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=log_name, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Load env variable from .env file
load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')
WELCOME_CHANNELS = ast.literal_eval(os.getenv('WELCOME_CHANNELS'))
print(WELCOME_CHANNELS)
with open('./TOKEN', 'r') as f:
    TOKEN = f.readline().strip()

# set intents to use (using default and setting members to true)
intents = discord.Intents.default()
intents.members = True
intents.typing = False

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """
    defines what to do when the bot is ready (connected and having received all informations needed)
    :return: None
    """
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:'
    )

    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')

    uitre_id = 316614281800187904
    if uitre_id in [member.id for member in guild.members]:
        channel = client.get_channel(873610728215547946)
        await channel.send(f'Salut mon best bro <@!{uitre_id}>, je suis connecté, allons chasser des lolis ensemble!')


@client.event
async def on_message(message):
    """
    defines what to do when a message is sent.
    :param message: discord.Message object
    :return: None
    """
    messages = {
        "loli": ['Où ça une loli?', 'Moi aussi j\'aime les lolis!'],
        "cul": ['C\'est ton cul que je vais prendre', 'Un cul :heart_eyes:'],
        "shota": ['Ara ara shouta-kun', 'Ici on préfère les lolis, les shota c\'est pour les pervers']
    }

    channel = message.channel
    if message.author == client.user:
        return

    if re.search('(?i)loli', message.content):
        await channel.send(random.choice(messages["loli"]))
    elif re.search('(?i)shou?ta', message.content):
        await channel.send(random.choice(messages["shota"]))
    elif re.search('(?i)cul', message.content):
        await channel.send(random.choice(messages["cul"]))


@client.event
async def on_member_join(member):
    """
    defines what to do when a member join a server.
    :param member: discord.Member object
    :return: None
    """
    guild = member.guild
    # get welcoming channel from WELCOME_CHANNELS, need to add int_guild_id: int_welcome_channel_id in .env file
    channel = client.get_channel(WELCOME_CHANNELS[guild.id])
    await channel.send(f'Bienvenue à toi <@!{member.id}>')


client.run(TOKEN)
