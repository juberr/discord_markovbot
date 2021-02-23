# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from markov_generator import generate


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = "$")


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command()
async def txt(ctx):
    
    msg = generate()
    await ctx.send(msg)


client.run(TOKEN)