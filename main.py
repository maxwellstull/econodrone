import os 
import discord 
from classes import App 
from secret_token import Token

def help_message():
    return """
Version 0.1 of econodrone, for tracking economy or economy-adjacent things in D&D.

Player Commands:
  ### GENERAL
    //save - Saves all current active content to json
    //me - prints user information
  ### MONEY
    //add --<unit> <amnt> - Adds money, unit is either 'p' for plat, 'g' for gold, or 'c' for copper.  
        Example: //add --g 10   will add 10 gold
        Example: //add --g 10 --p 1 will add 10 gold and 1 platinum
    //remove --<unit> <amnt> - Removes money, see "add" for units
        Example: Same formats as add
    //balance - Bot will print out your current balance
    //pay_player --<unit> <amnt> - Will spawn a context menu to choose player to send the money to
        Example: //pay_player --g 10 --p 1
  ### FOOD
    //add_ration <amnt> - Adds rations to inventory
        Example: //add_ration 4 will add 4 rations
    //remove_ration <amnt> - removes rations from inventory
        Example: No.
    //add_water <amnt> - Adds water to inventory
        Example: See above.
    //drink_water <amnt> - Slurp slurp slurp slurp

Sudo Commands (require elevated rights):
    //load - Loads content from json, OVERWRITING whatever is there
    //next_day - Removes 1 ration and 1 water from all
    //audit - Prints all players //me's
    """



client = discord.Client(intents=discord.Intents.all())
appy = App()

@client.event 
async def on_ready():
    appy.load_json()

@client.event 
async def on_message(message):
    if message.author.id != 1092864433014968360:
        if str(message.guild.id) not in appy.servers:
            print("Shit, we need a new server dict")
            appy.add_server(str(message.guild.id))
        if str(message.author.id) not in appy.servers[str(message.guild.id)].users:
            print("Adding new users")
            appy.add_user(message)
        if message.content.startswith("//"):
            payload = message.content.replace("//","")
            payload = payload.split(" ")
            print(payload)
            command = payload[0]
            match command:
                case "save":
                    appy.save_json()
                case "load":
                    appy.load_json()
                case "me":
                    print("Me detected")
                    await message.channel.send(appy.print_user(message))
                case "help":
                    await message.channel.send(help_message())
    else:
        print("Get outta here")

client.run(Token().token)

