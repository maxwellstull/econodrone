import os 
import discord 
from classes import App 
import shlex
from secret_token import Token

def help_message():
    return """
Version 0.1 of econodrone, for tracking economy or economy-adjacent things in D&D.

Player Commands:
  **GENERAL**
    Typical commands.
    `//save` - Saves all current active content to json
    `//me` - prints user information
  **MONEY**
    All commands relating to money.
    `//add --<unit> <amnt>` - Adds money, unit is either 'p' for plat, 'g' for gold, or 'c' for copper.  
    `//remove --<unit> <amnt>` - Removes money, see "add" for units
    `//balance` - Bot will print out your current balance
  **FOOD**
    All commands relating to food.
    `//add_ration <amnt>` - Adds rations to inventory
    `//eat_ration <amnt>` - removes rations from inventory
  **HEALTH**
    All command relating to health.
    `//set_max_hp <amnt>` - Sets your maximum hp
    `//set_hp <amnt>` - Sets your current hp
    `//heal <amnt>` - Regenerate some health
    `//damage <amnt>` - Take damage
  **SPELLS**
    Slot management. Along with spell slots, this can work for any class's points.
        To do this, instead of a level, put what kind of point it is. It'll track it.
    `//add_slots --<level> <amnt>` - Adds spell slots
    `//set_slots --<level> <amnt>` - Overrides to the amount. Only supports 1 level at a time.
    `//spell <level>` - Consumes 1 spell slot of that level
    `//regenerate --<level> <amnt>` - Regerate specific slots
  **Sudo Commands** (require elevated rights):
    `//load` - Loads content from json, OVERWRITING whatever is there
    `//next_day` - Removes 1 ration and 1 water from all
    `//audit` - Prints all players //me's
    `//long_rest` - Runs long rest on players health and spell slots
    """





BOT_ID = 1092864433014968360
OP_ID = 397851620408426506

client = discord.Client(intents=discord.Intents.all())
appy = App()

@client.event 
async def on_ready():
    appy.load_json()

@client.event 
async def on_message(message):
    if message.author.id != BOT_ID:
        if str(message.guild.id) not in appy.servers:
            print("Shit, we need a new server dict")
            appy.add_server(str(message.guild.id))
        if str(message.author.id) not in str(appy.servers[str(message.guild.id)].users.keys()):
            print("Adding new users")
            appy.add_user(message)
        if message.content.startswith("//"):
            payload = message.content.replace("//","")
            payload = shlex.split(payload)
            print("Payload:",payload)
            command = payload[0]
            guild_id = str(message.guild.id)
            user_id = str(message.author.id)

            match command:
                case "save":
                    appy.save_json()
                case "me":
                    await message.channel.send(appy.servers[guild_id].users[user_id])
                case "help":
                    await message.channel.send(help_message())
                case "add":
                    appy.servers[guild_id].users[user_id].compute_currency(payload, 1)
                case "remove":
                    appy.servers[guild_id].users[user_id].compute_currency(payload, -1)
                case "balance":
                    await message.channel.send(appy.servers[guild_id].users[user_id].currency)
                case "add_ration":
                    appy.servers[guild_id].users[user_id].compute_ration(payload, 1)
                case "eat_ration":
                    appy.servers[guild_id].users[user_id].compute_ration(payload, -1)
                case "set_max_hp":
                    appy.servers[guild_id].users[user_id].set_max_health(payload)
                case "set_hp":
                    appy.servers[guild_id].users[user_id].set_hp(payload)
                case "heal":
                    appy.servers[guild_id].users[user_id].compute_health(payload, 1)
                case "damage":
                    appy.servers[guild_id].users[user_id].compute_health(payload, -1)
                case "long_rest":
                    appy.servers[guild_id].long_rest()
                case "add_slots":
                    appy.servers[guild_id].users[user_id].add_slots(payload)
                case "set_slots":
                    appy.servers[guild_id].users[user_id].set_slots(payload)
                case "spell":
                    appy.servers[guild_id].users[user_id].spell(payload)
                case "regenerate":
                    appy.servers[guild_id].users[user_id].regenerate(payload)
                case "add_item":
                    appy.servers[guild_id].users[user_id].add_item(payload)
                case "next_day" if user_id == OP_ID:
                    appy.servers[guild_id].next_day()
                case "audit" if user_id == OP_ID:
                    await message.channel.send(appy.servers[guild_id].audit(message))
                case "load" if user_id == OP_ID:
                    appy.load_json()
            await message.add_reaction("\U0001F62B")

client.run(Token().token)

