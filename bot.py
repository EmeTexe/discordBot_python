# main.py
import os
import sys

from discord.ext import commands
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

prefix = '159'

bot = commands.Bot(command_prefix=prefix, intents=intents)

messages = {
    "loli": ['Où ça une loli?', 'Moi aussi j\'aime les lolis!'],
    "cul": ['C\'est ton cul que je vais prendre', 'Un cul :heart_eyes:'],
    "shota": ['Ara ara shouta-kun', 'Ici on préfère les lolis, les shota c\'est pour les pervers']
}


@bot.event
async def on_ready():
    """
    defines what to do when the bot is ready (connected and having received all informations needed)
    :return: None
    """
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:'
    )

    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')

    uitre_id = 316614281800187904
    if uitre_id in [member.id for member in guild.members]:
        channel = bot.get_channel(873610728215547946)
        # await channel.send(f'Salut mon best bro <@!{uitre_id}>, je suis connecté, allons chasser des lolis ensemble!')
        await channel.send('Connecté, et prêt à chasser des lolis!')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print('new message')
    """
    defines what to do when a message is sent.
    :param message: discord.Message object
    :return: None
    """

    channel = message.channel
    if message.author == bot.user:
        return
    if message.content[0:len(prefix)] == prefix:
        return
    else:
        print(f'False for message:\n{message.content}')
    if re.search('(?i)loli', message.content):
        await message.reply(random.choice(messages["loli"]), mention_author=False)
        # await channel.send(random.choice(messages["loli"]))
    elif re.search('(?i)shou?ta', message.content):
        await message.reply(random.choice(messages["shota"]), mention_author=False)
        # await channel.send(random.choice(messages["shota"]))
    elif re.search('(?i)cul', message.content):
        await message.reply(random.choice(messages["cul"]), mention_author=False)
        # await channel.send(random.choice(messages["cul"]))


@bot.event
async def on_member_join(member):
    """
    defines what to do when a member join a server.
    :param member: discord.Member object
    :return: None
    """
    guild = member.guild
    # get welcoming channel from WELCOME_CHANNELS, need to add int_guild_id: int_welcome_channel_id in .env file
    channel = bot.get_channel(WELCOME_CHANNELS[guild.id])
    await channel.send(f'Bienvenue à toi <@!{member.id}>')


@bot.command(name='loli', help='Choisi une phrase à répondre en lien avec les lolis')
async def answer_loli(ctx):
    await ctx.send(random.choice(messages["loli"]))


@bot.command(name='shota', help='Choisi une phrase à répondre en lien avec les shotas')
async def answer_shota(ctx):
    await ctx.send(random.choice(messages["shota"]))


@bot.command(name='cul', help='Choisi une phrase à répondre en lien avec les culs')
async def answer_cul(ctx):
    await ctx.send(random.choice(messages["cul"]))


@bot.command(name='milf', help='Choisi une phrase à répondre en lien avec les milfs')
async def answer_milf(ctx):
    await ctx.send('Ara ara')


@bot.command(name='obfuscate', help='Prend la phrase suivant la commande et met certaines lettres au hasard en majuscule ou minuscule.')
async def obfuscate(ctx, *args):
    s = " ".join(args[:])
    answer = ''
    for c in s:
        r = random.random()
        if r<0.5:
            c = c.lower()
        else:
            c = c.upper()
        answer += c
    await ctx.send(answer)

bot.run(TOKEN)
