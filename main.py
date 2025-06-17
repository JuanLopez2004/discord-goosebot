#library imports
import discord
from discord.ext import commands
from discord.ui import View, Button
import logging 
from dotenv import load_dotenv
import os
import requests
import random
from discord import Spotify

## Time and Date Import libraries
import datetime
import asyncio
import time  
import pytz
from discord.ext import tasks

# Sets the timezone to central chicago 
CENTRAL_TZ = pytz.timezone('US/Central') 
last_sent_date = None  # To avoid duplicate messages

## For Skramz Feature
skramz_artists = {

    "Orchid", "Pg.99", "Saetia", "City of Caterpillar", "I Hate Myself",
    "Jeromes Dream", "William Bonney", "Merchant Ships", "Your Arms Are My Cocoon", "Flowers Taped To Pens", 
    "iwrotehaikusaboutcannibalisminyouryearbook", "Funeral Diner", "Suis La Lune", 
}

user_cooldowns = {}
COOLDOWN_SECONDS = 240

#################################################

# Load environment variables from .env file
load_dotenv()
token = os.getenv("DISCORD_TOKEN") ##loads token from .env file

## Intent handling for message content and members
############################################################

handler = logging.FileHandler(filename='discord.log', encoding="utf8", mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

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
    print(f"LOGGED INTO GOOSEBOT!")
    if not night_message.is_running():
        night_message.start()

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
    embed.add_field(name="!spaghetti", value="Shows an image of Hotel Mario", inline=False)
    embed.add_field(name="!goose", value="Shows a little Goose game", inline=False)
    embed.add_field(name="!pfp @user", value="Shows Selected User's Profile Picture", inline=False)

    await ctx.send(embed=embed)         #Sends the embed to the channel

###########################################################


##nate !kill command
###########################################################

@bot.command(name='kill')                                 # bot.command() is the decorator that registers the func as a command
async def kill_command(ctx):                              # context is the object passed to every command function    
    await ctx.send("must kill nate!!!!")

###########################################################


#!dinner command
##sends an image of the king 
###########################################################

@bot.command(name="dinner")
async def dinner_command(ctx):           
    file = discord.File(r"C:\Users\radis\discord-goosebot\images\king.jpg", filename="king.jpg")   # Loads the image file from the specified path
    embed = discord.Embed(title="King")                                                            # Creates an embed object with the title "King"
    embed.set_image(url="attachment://king.jpg")                                                   # must match filename
    await ctx.send(file=file, embed=embed)                                                         # sends the file and embed to the channel
                                                                                                   # THIS SHOULD BE the standard for sending images, gifs, embeds to discord
###########################################################


## Spaghetti Command
###########################################################

@bot.command(name="spaghetti")
async def spaghetti_command(ctx):        
    file = discord.File(r"C:\Users\radis\discord-goosebot\images\spaghetti.jpg", filename="spaghetti.jpg")
    embed = discord.Embed(title="Spaghetti")
    embed.set_image(url="attachment://spaghetti.jpg")
    await ctx.send(file=file, embed=embed)
    await ctx.send("I HOPE SHE MADE LOTSA SPAGHETTI!")

###########################################################


## Goose Game
###########################################################

## Class for the button embed
class gooseView(View):
    def __init__(self): ## 
        super().__init__(timeout=None) ##
        
    @discord.ui.button(label="Pet the Goose", style=discord.ButtonStyle.primary)
    async def pet_goose(self, interaction:discord.Interaction, button: discord.ui.Button):
        file = discord.File(r"C:\Users\radis\discord-goosebot\images\gooseat.jpg",filename="gooseat.jpg")
        embed = discord.Embed(title="the goose is ANGRY")
        embed.set_image(url="attachment://gooseat.jpg")
        await interaction.response.send_message(file=file, embed=embed)


@bot.command(name="goose")
async def goose_command(ctx):
    file = discord.File(r"C:\Users\radis\discord-goosebot\images\goose.gif", filename="goose.gif")
    embed = discord.Embed(title="goose")
    embed.set_image(url="attachment://goose.gif")

    view = gooseView()                                                    #
    await ctx.send(file=file, embed=embed, view=view)
    await ctx.send("HONK HONK HONK HONK HONK")

##########################################################


##user profile picture commands
##########################################################

@bot.command(name="pfp")
async def pfp_command(ctx, member: discord.Member):
    await ctx.send(member.display_avatar)

##########################################################


## Nightly Message
##########################################################

@tasks.loop(minutes=1)
async def night_message(): 
    global last_sent_date # To keep track of the last sent date
    
    now = datetime.datetime.now(pytz.utc)           # Get current time in UTC
    central_now = now.astimezone(CENTRAL_TZ)        # Convert to Central Time

    if central_now.hour == 20 and central_now.minute == 30:  # Check if it's 8:30 PM Central Time
        if last_sent_date != central_now.date():             # Check if the message has already been sent today
            channel = bot.get_channel(689005693621239848)    # General channel ID 
            if channel:                                      # If the channel is found
                file = discord.File(r"C:\Users\radis\discord-goosebot\images\nightcore..gif", filename="nightcore..gif")  # Load the GIF file with filepath
                embed = discord.Embed(title="ng2")                        
                embed.set_image(url="attachment://nightcore..gif")      # Create an embed object, sets image, and then sends the file and embeds       
                await channel.send(file=file, embed=embed)          
                last_sent_date = central_now.date()              # Mark as sent for today before the next loop

@night_message.before_loop          # This function runs before the loop starts
async def before_night_message():
    await bot.wait_until_ready()

##########################################################


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


### Skramz
###########################################################

@bot.event
async def on_presence_update(before, after):
    if after.activity and isinstance(after.activity, discord.Spotify):
        activity = after.activity
        artist = activity.artist

        now = time.time()
        last_triggered = user_cooldowns.get(after.id, 0)
        if now - last_triggered < COOLDOWN_SECONDS:
            return  # cool down
        user_cooldowns[after.id] = now  # update the last time it was used

        if artist in skramz_artists:  # if artist is in skramz list
            channel = discord.utils.get(after.guild.text_channels, name="general") # send to general
            if channel: 
                await channel.send(
                    f"{after.mention} is listening to skramz. "
                    f"HEY SKRAMZ KID WE LISTEN TO MATH ROCK AROUND HERE! "
                    f"({activity.title} by {artist})"
                )

###########################################################

###print(f"TOKEN LOADED: {token}")
bot.run (token, log_handler=handler, log_level=logging.DEBUG)