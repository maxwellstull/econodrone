import os 
import discord 
from classes import App 
TOKEN = "MTA5Mjg2NDQzMzAxNDk2ODM2MA.GqUsW7.AQNtgoONaexy9FdGEWdEwQJWhnXfx1O0GfHVnM"

client = discord.Client(intents=discord.Intents.all())
appy = App()


@client.event 
async def on_ready():
    appy.load_json()

@client.event 
async def on_message(message):
    if message.author.id not in appy.users:
        appy.add_user(message.author)
    if message.content.startswith("//"):
        payload = message.content.replace("//","")
        payload = payload.split(" ")
        print(payload)

#    print(message)
#    print(message.author.id)
#    print(message.author.name)

client.run(TOKEN)

