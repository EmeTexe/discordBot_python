# main.py
import os
import sys
import json
import requests

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

with open('./TOKEN', 'r') as f: TOKEN = f.readline().strip()

with open('./tenor_key', 'r') as f: TENOR_KEY = f.readline().strip()

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


# Working on it, will be integrated in on_ready()
def get_tenor_gifs_results(query: str = "smile", limit: int = 20, contentfilter: str = 'off', locale: str = 'en_US',
                           media_filter: str = 'minimal', ar_range: str = 'all'):
    req = f"https://g.tenor.com/v1/search?key={TENOR_KEY}&q={query}&limit={limit}&locale={locale}&contentfilter={contentfilter}&media_filter={media_filter}&ar_range={ar_range}"
    r = requests.get(req)
    if r.status_code == 200:
        gifs = json.loads(r.content)["results"]
        return [i['url'] for i in gifs]
    else:
        return None


@bot.event
async def on_ready():
    """
    defines what to do when the bot is ready (connected and having received all informations needed)
    :return: None
    """

    print(
        f'{bot.user} is connected to the following guild:'
    )

    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')

    guild = discord.utils.get(bot.guilds, name=GUILD)
    category = discord.utils.get(guild.categories, name='share gif')

    channel = bot.get_channel(873610728215547946)
    await channel.send('Connecté, et prêt à chasser des lolis!')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
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


@bot.command(name='obfuscate',
             help='Prend la phrase suivant la commande et met certaines lettres au hasard en majuscule ou minuscule.')
async def obfuscate(ctx, *args):
    s = " ".join(args[:])
    answer = ''
    for c in s:
        r = random.random()
        if r < 0.5:
            c = c.lower()
        else:
            c = c.upper()
        answer += c
    await ctx.send(answer)


@bot.command(name='ban', help='Ban l\'utilisateur spécifié pour la raison spécifiée.')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason: str = "Pour aucune raison, la gratuité"):
    if not member:
        await ctx.channel.send("Vous ne pouvez pas ban personne")
        return
    await ctx.channel.send(f"{member.display_name} a été banni pour la raison suivante :\n{reason}")
    await member.ban()


@bot.command(name='kick', help='Ban l\'utilisateur spécifié pour la raison spécifiée.')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason: str = "Aucune raison, la gratuité"):
    if not member:
        await ctx.channel.send("Vous ne pouvez pas kick personne")
        return
    await ctx.channel.send(f"{member.display_name} a été kick pour la raison suivante :\n{reason}")
    await member.kick()


@bot.command(name='unban', help='Enlève le bannissement de la personne concernée.')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member: str = None):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    print(member)

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            print(f"{member} found")
            await ctx.guild.unban(user)
            await ctx.send(f'Le bannissement de {user.mention} a été révoqué.')
            return
    else:
        await ctx.send(f'Le bannissement de {member_name}#{member_discriminator} n\'a pas pu être révoqué')


@bot.command(name='gif', help='Cherche un gif contenant les mots souhaités')
async def gif(ctx, *, recherche):
    print(recherche)
    result = get_tenor_gifs_results(recherche)
    if result:
        send = random.choice(result)
        if send[0:4] == 'http':
            await ctx.send(send)
        else:
            await ctx.send(f"Impossible de trouver un gif correspondant à la recherche \"{recherche}\"")
    else:
        await ctx.send(f"Impossible de trouver un gif correspondant à la recherche \"{recherche}\"")


bot.run(TOKEN)
