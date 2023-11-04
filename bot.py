import discord
from discord.ext import commands
from random import *
import discord
from discord.ext import commands,tasks
import os
from flask import *
import requests
import bs4
from bs4 import BeautifulSoup
import random
from random import randrange
from steammethods import *

app = Flask(__name__) 

if __name__=='__main__':
   app.run()

def run_discord_bot():
    TOKEN = "MTE1MTY1NjQ3ODk3ODA4MDg1OQ.GCxVH0.TPC0GDVSI2d87tyle_vxD1e37CdgxR7FRZ4AYo"
    client = discord.Client(command_prefix='!',intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        print('Current Directory: ' + os.getcwd())
        
    @client.event
    async def on_message(message):
        if message.content.startswith('!'):
            items = message.content.split()
            match items[0]:
                case '!help':
                    await message.channel.send("Commands: !teamgen gameName, !sale gameName, !ratings gameName, !random category")
                case '!teamgen':
                    await message.channel.send("\n".join(teamgen_command(message)))
                case '!sale':
                    await message.channel.send(sale_command(message))
                case '!ratings':
                    await message.channel.send(ratings_command(message))
                case "!random":
                    await message.channel.send(random_command(message))
    client.run(TOKEN)


@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("fname")
       # getting input with name = lname in HTML form
       last_name = request.form.get("lname")
       input = first_name + " " + last_name
       # write to text file
       with open("LatestMessage.txt", "w") as text_file:
            text_file.write(input)
       return "Your name is "+first_name + last_name + ", Sending data somewhere. "
    return render_template("form.html")
