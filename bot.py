# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from markov_generator import generate
import json 


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = "$")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='gameing'))
    print(f'{client.user} has connected to Discord!')

@client.command()
async def helpme(ctx):
    msg = "Currently I can:\n$txt - Generate a random message from our tweets\n$highlight: save a randomly generated message to our bot highlights channel"
    await ctx.send(msg)


@client.command()
async def txt(ctx):

    msg = generate()

    with open("last_message.txt", "w") as last_message:
        last_message.write(msg)

    print(f"{ctx.guild} generated: {msg}")
    await ctx.send(msg)

@client.command()
async def highlight(ctx):
    # posts the previous message to a highlights channel, only allows for one highlight.

    channel = client.get_channel(814928637496393778)

    prev_message = await channel.fetch_message(channel.last_message_id)

    
    try:
        with open("last_message.txt", "r") as lm:
            highlight = lm.read()[1:]
        
        if highlight == prev_message.content:
            await ctx.send("This message has already been highlighted!")
        else:
            await channel.send(highlight)
            
# if no messages have been sent, this except block will catch that
    except:
        await ctx.send("Sorry, no previous message saved!")

    

    


client.run(TOKEN)