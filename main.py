##library imports
import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import requests
import random

load_dotenv()
token = os.getenv("DISCORD_TOKEN") ##loads token

## Intent handling for message content and members
############################################################

handler = logging.FileHandler(filename='discord.log', encoding="utf8", mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

############################################################


## !Prefix and Help commands
############################################################

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")  

############################################################


## when main.py is ran, displays login message to indicate bot is online
############################################################

@bot.event 
async def on_ready():
    print(f"Logged in")

############################################################


### Features
### Whenever a word is said it repeats a phrase ############ DOESNT WORK
############################################################

@bot.event
async def on_message(message):
    print(f"DEBUG: Received message: {message.content}")

    if message.author == bot.user:
        return

    if message.content.lower() == "sazo":
        await message.channel.send("😭😭😭😭😭😭 <@720767180517539890>")
    
    await bot.process_commands(message)

###########################################################


#help command list that shows all commands 
###########################################################

@bot.command(name='help')
async def help_command(ctx):             #help_command function
    embed = discord.Embed(               #Creates embed object
        title="Help Commands List",
        color=discord.Color.blue() 
            )

    #Add commands here
    embed.add_field(name="!kill", value="Kills Nate", inline=False)
    embed.add_field(name="!dinner", value="Shows the King", inline=False)
    embed.add_field(name="!spaghetti", value="shows luigi", inline=False)

    await ctx.send(embed=embed)         #Sends the embed to the channel

###########################################################


##nate !kill command
###########################################################

@bot.command(name='kill')
async def kill_command(ctx):
    await ctx.send("must kill nate!!!!")

###########################################################

#!dinner command
##sends an image of the king 
###########################################################

@bot.command(name="dinner")
async def dinner_command(ctx):
    file = discord.File(r"C:\Users\radis\discordbot\images\king.jpg", filename="king.jpg")
    embed = discord.Embed(title="King")
    embed.set_image(url="attachment://king.jpg")  # must match filename
    await ctx.send(file=file, embed=embed)

###########################################################


## Spaghetti Command
###########################################################

@bot.command(name="spaghetti")
async def spaghetti_command(ctx):
    file = discord.File(r"C:\Users\radis\discordbot\images\spaghetti.jpg", filename="spaghetti.jpg")
    embed = discord.Embed(title="Spaghetti")
    embed.set_image(url="attachment://spaghetti.jpg")
    await ctx.send(file=file, embed=embed)
    await ctx.send("I HOPE SHE MADE LOTSA SPAGHETTI!")

###########################################################


## message logger
###########################################################

def log_message(message):
    with open("message_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(
            f"[{message.created_at}] {message.author} in #{message.channel}: {message.content}\n"
        )

###########################################################


### auto logger
###########################################################

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    log_message(message)
    await bot.process_commands(message)

###########################################################


##run/testing
###print(f"TOKEN LOADED: {token}")
bot.run (token, log_handler=handler, log_level=logging.DEBUG)