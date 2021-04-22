# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from markov_generator import generate
from jep_functions import parse_jep
import asyncio
import json 
import requests
import time
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = "$")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='gameing'))
    print(f'{client.user} has connected to Discord!')

@client.command()
async def helpme(ctx):
    msg = "Currently I can:\n$txt - Generate a random message from our tweets\n$highlight - save a randomly generated message to our bot highlights channel"
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


@client.command()
@commands.cooldown(1, 11, commands.BucketType.user)
async def jep(ctx):
    await client.change_presence(activity=discord.Game(name='jep'))
    valid_starts = ['what is', 'who is', 'when is', 'where is']
    
    # get a jeopardy question using the jservice.io
    jep = requests.get('http://jservice.io/api/random').json()

    #parse json with premade function
    question, value, category, answer = parse_jep(jep)

    # create a discord message to present question
    q =  f'''
```Category: {category}

Value: {value}

Clue: {question}
```
    '''
    print(answer)

    # send the message
    await ctx.send(embed=discord.Embed(description=q, title='This, is Jeopardy!'))

    # begin the j! game
    time_start = time.time()

    channel = client.get_channel(814931872987217940)

    while True:

        #function to ensure message is coming from the correct channel
        def check(msg):
            return msg.channel == channel
  
        try:
            # wait for responses with 10 second timeout
            prev_message = await client.wait_for("message", check=check, timeout=20)

            usr_ans = str(prev_message.content)

            usr_start = ' '.join(usr_ans.split()[0:2])

            # if valid jep answer
            if usr_start in valid_starts:

                valid_ans = ' '.join(usr_ans.split()[2:])
                print(valid_ans)

                # if correct
                if valid_ans == answer.lower():
                    await ctx.send(f'That\'s it {prev_message.author.mention}!')
                    await client.change_presence(activity=discord.Game(name='gameing'))
                    break

                # if wrong
                else:

                    await ctx.send(f'mmmm sorry, no {prev_message.author.mention}')     
            
        # if no answers      
        except asyncio.TimeoutError:
            await client.change_presence(activity=discord.Game(name='gameing'))
            await ctx.send(f'**Beep Beep Beep!** The answer was "{answer}"')
            break     


   
                
            








client.run(TOKEN)