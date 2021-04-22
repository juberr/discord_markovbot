# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from markov_generator import generate
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

    valid_starts = ['what is', 'who is', 'when is', 'where is']
    
    # get a jeopardy question using the jservice.io
    jep = requests.get('http://jservice.io/api/random').json()

    # create a discord message to present question
    q =  f'''
```Topic: {jep[0]['category']['title']}

Value: {jep[0]['value']}

Question: {jep[0]['question']}

ANSWER: REMOVE LATER {jep[0]['answer']}
```
    '''
    print(q)

    # send the message
    await ctx.send(q)

    # begin the j! game
    time_start = time.time()

    channel = client.get_channel(812424668320497717)

    while True:
        
        prev_message = await channel.fetch_message(channel.last_message_id)

        print(prev_message)
        
        if str(prev_message.author.name) != 'toesnshots.txt':
            
            usr_ans = str(prev_message.content)

            usr_start = ' '.join(usr_ans.split()[0:2])

            if usr_start in valid_starts:
                valid_ans = ' '.join(usr_ans.split()[2:])
                corr_answer = jep[0]['answer'].lower()
                print(valid_ans)

                if valid_ans == corr_answer:
                    await ctx.send(f'grats {prev_message.author.mention}')
                    break

        if time.time() >= time_start + 15:
            corr_answer = jep[0]['answer']
            await ctx.send(f'**Beep Beep Beep!** The answer was "{corr_answer}"')
            break        
                
            








client.run(TOKEN)