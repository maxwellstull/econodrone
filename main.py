import os 
import discord 
from classes import App 
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
        if str(message.author.id) not in str(appy.servers[str(message.guild.id)].users.keys()):
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
                    if message.author.id == 397851620408426506:
                        appy.load_json()
                    else:
                        await message.channel.send("Fuck off you don't have permission to do this")
                case "me":
                    await message.channel.send(appy.print_user(message))
                case "help":
                    await message.channel.send(help_message())
                case "add":
                    appy.add(message, payload)
                case "remove":
                    appy.remove(message, payload)
                case "balance":
                    await message.channel.send(appy.servers[str(message.guild.id)].users[str(message.author.id)].currency)
                case "add_ration":
                    appy.add_ration(message,payload)
                case "eat_ration":
                    appy.remove_ration(message,payload)
                case "add_water":
                    appy.add_water(message,payload)
                case "drink_water":
                    appy.drink_water(message,payload)
                case "set_max_hp":
                    appy.set_max_health(message,payload)
                case "set_hp":
                    appy.set_hp(message, payload)
                case "heal":
                    appy.heal(message,payload)
                case "damage":
                    appy.damage(message,payload)
                case "long_rest":
                    appy.long_rest(message,payload)
                case "add_slots":
                    appy.add_slots(message, payload)
                case "set_slots":
                    appy.set_slots(message,payload)
                case "spell":
                    appy.spell(message, payload)
                case "regenerate":
                    appy.regenerate(message, payload)
                case "next_day":
                    if message.author.id == 397851620408426506:
                        appy.next_day(message)
                    else:
                        await message.channel.send("Fuck off you don't have permission to do this")
                case "audit":
                    if message.author.id == 397851620408426506:
                        await message.channel.send(appy.audit(message))
                    else:
                        await message.channel.send("Fuck off you don't have permission to do this")
            await message.add_reaction("\U0001F62B")

client.run(Token().token)

