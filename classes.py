import json

# App class, holds all the servers
class App():
    # Creation
    def __init__(self) -> None:
        # Dict of all servers the bot is in. Users have different profiles based on server
        self.servers = {}
    # Add users to the server they sent a message from
    def add_user(self, message):
        self.servers[str(message.guild.id)].add_user(message)
    # Adds a new server
    def add_server(self, id):
        self.servers[id] = Server(id)
    ## Save / Load ##
    def load_json(self):
        fp = open("savedata.json","r")
        to_load = json.load(fp)
        for server_id, server in to_load.items():
            self.servers[server_id] = Server(server_id)
            self.servers[server_id].load_json(server)
        print("Json Loaded")
    def save_json(self):
        to_save = {}
        for server_id, server in self.servers.items():
            print(server_id, server)
            to_save[server_id] = server.save_json()
        with open("savedata.json","w") as fp:
            json.dump(to_save, fp)



        
        

class Server():
    def __init__(self,id) -> None:
        self.users = {}
        self.id = id
    def load_json(self, json_data):
        self.id = json_data['id']
        for user_id, user in json_data['users'].items():
            self.users[user_id] = User()
            self.users[user_id].load_json(user)
    def save_json(self):
        to_save = {}
        to_save['id'] = self.id
        user_info = {}
        for user_id, user in self.users.items():
            user_info[user_id] = user.save_json()
        to_save['users'] = user_info
        return to_save
    def add_user(self, message):
        print("Adding server user")
        self.users[str(message.author.id)] = User(message.author.id, message.author.name, message.author.nick)
    def __repr__(self):
        return "User Ct: {ct}".format(ct=len(self.users))
    def long_rest(self):
        for user_id, user in self.users.items():
            user.long_rest()
    def audit(self):
        retval = ""
        for _id, user in self.users.items():
            retval += str(user)
            retval += "\n\n"
        return retval
    def next_day(self):
        for user in self.users:
            user.rations.food = user.rations.food - 1
class User():
    def __init__(self, id=0, name="", nick="") -> None:
        self.id = id 
        self.name = name
        self.nick = nick
        self.maxhealth = 0
        self.health = 0
        self.currency = Money()
        self.rations = Ration()
        self.spells = SpellSlots()
        self.inv = Inventory()
    def load_json(self, json_data):
        self.id = json_data['id']
        self.name = json_data['name']
        self.nick = json_data['nick']
        self.health = int(json_data['health'])
        self.maxhealth = int(json_data['maxhealth'])
        self.currency.load_json(json_data['currency'])
        self.rations.load_json(json_data['rations'])
        self.spells.load_json(json_data["spellslots"])
        self.inv.load_json(json_data['inventory'])
    def save_json(self):
        return {"id":self.id, 
                "name":self.name, 
                "nick":self.nick, 
                "health":self.health,
                "maxhealth":self.maxhealth,
                "currency":self.currency.save_json(), 
                "rations":self.rations.save_json(),
                "spellslots":self.spells.save_json(),
                "inventory":self.inv.save_json()}
    def __repr__(self) -> str:
        return """
        Name: {nm}
        Nick: {nk}
            Health: {h}/{mh}
            Money: {m}
            Ration: {r}
        Slots:\n{ss}
        """.format(nm = self.name, nk=self.nick, m=str(self.currency), r=str(self.rations),h=self.health,mh=self.maxhealth, ss=str(self.spells))
    # Computation
    def compute_currency(self, payload, modifier):
        for i in range(1, len(payload), 2):
            coin_type = payload[i].replace("--","")
            coin_amnt = int(payload[i+1])
            match coin_type:
                case "p":
                    self.currency.plat = self.currency.plat + modifier*coin_amnt
                case "g":
                    self.currency.gold = self.currency.gold + modifier*coin_amnt
                case "c":
                    self.currency.copper = self.currency.copper + modifier*coin_amnt    
    def compute_ration(self, payload, modifier):
        self.rations.food += modifier*int(payload[1])
    def compute_health(self, payload, modifier):
        self.health += modifier*int(payload[1])
    #Health
    def set_max_health(self, payload):
        self.maxhealth = payload[1]
    def set_hp(self, payload):
        self.health = payload[1]
    #Slots
    def add_slots(self, payload):
        for i in range(1, len(payload), 2):
            level = payload[i].replace("--","")
            amnt = payload[i+1]
            self.spells.add_slots(level, amnt)
    def set_slots(self, payload):
        level = payload[1]
        amnt = payload[2]
        self.spells.set_slots(level, amnt)
    def spell(self, payload):
        level = payload[1]
        self.spells.use(level)
    def regenerate(self, payload):
        for i in range(1, len(payload), 2):
            level = payload[i].replace("--","")
            amnt = payload[i+1]
            self.spells.regenerate(level, amnt)
    def long_rest(self):
        self.health = self.maxhealth
        self.spells.long_rest()
    def add_item(self, payload):
        self.inv.add_item(payload)
class Money():
    def __init__(self) -> None:
        self.copper = 0
        self.gold = 0
        self.plat = 0
    def __repr__(self) -> str:
        retval = "[{pl}p,{gp}g,{cu}c]".format(pl=self.plat, gp=self.gold, cu=self.copper)
        return retval 
    def save_json(self):
        return {"p":self.plat, "g":self.gold, "c":self.copper}
    def load_json(self, json_data):
        self.copper = json_data['c']
        self.gold = json_data['g']
        self.plat = json_data['p']
class Ration():
    def __init__(self) -> None:
        self.food = 0
    def __repr__(self) -> str:
        retval = "[{fd} meals]".format(fd=self.food)
        return retval
    def save_json(self):
        return {"meals":self.food}
    def load_json(self, json_data):
        self.food = json_data['meals']
class SpellSlots():
    def __init__(self) -> None:
        self.slots = {}
    def __repr__(self) -> str:
        retval = ""
        for level in sorted(list(self.slots.keys())):
            retval += "\t\t\t{le}: {ss}\n".format(le=level,ss=self.slots[level])
        return retval
    def save_json(self):
        retval = {}
        for key, value in self.slots.items():
            retval[key] = value.save_json()
        return retval
    def load_json(self, json_data):
        for key in json_data.keys():
            self.slots[key] = SpellSlot() 
            self.slots[key].load_json(json_data[key])
    def add_slots(self, level, amnt):
        if level in self.slots.keys():
            self.slots[level].total += int(amnt)
        else:
            self.slots[level] = SpellSlot()
            self.slots[level].total = int(amnt)
    def set_slots(self, level, amnt):
        self.slots[level].total = int(amnt)
    def use(self, level):
        self.slots[level].use()
    def regenerate(self, level, amnt):
        self.slots[level].regenerate(amnt)
    def long_rest(self):
        for level, spells in self.slots.items():
            spells.used = 0
class SpellSlot():
    def __init__(self) -> None:
        self.used = 0
        self.total = 0
    def __repr__(self) -> str:
        retval = "`"
        for _ in range(0, self.used):
            retval += "(x)"
        for _ in range(0, (self.total-self.used)):
            retval += "( )"
        return retval +"`"
    def save_json(self):
        return {"used":self.used, "total":self.total} 
    def load_json(self, json_data):
        self.used = json_data['used']
        self.total = json_data['total']
    def use(self):
        self.used += 1
    def regenerate(self, amnt):
        self.used -= int(amnt)
        if self.used < 0:
            self.used = 0
class Inventory:
    def __init__(self) -> None:
        # Name and object
        self.items = {}
        # Number and name
        self.alias = {}
        cur_num = 1
        pass
    def __repr__(self) -> str:
        retval = ""
        for number, name in self.alias.items():
            retval += "{num}: {item}".format(num=number, name=self.items[name])
    def save_json(self):
        retval = {}
        ret_items = {}
        for key, value in self.items.items():
            ret_items[key] = value.save_json()
        retval['items'] = ret_items
        retval['alias'] = self.alias
        return retval
    def load_json(self, json_data):
        for key in json_data['items'].keys():
            self.items[key] = Item()
            self.items[key].load_json(json_data['items'][key])
        self.alias = json_data['alias']
    def add_item(self,payload):
        new_item = Item()
        new_item.name = payload[1]
        for i in range(2, len(payload), 2):
            attr = payload[i]
            data = payload[i+1]
            print(attr, data)
            match attr:
                case "amnt":
                    new_item.amnt = data
                case "w" | "weight":
                    new_item.weight = data
                case "v" | "val" | "value":
                    new_item.value = data
                case "d" | "desc":
                    new_item.desc = data
        self.items[new_item.name] = new_item
    def edit(self, payload):
        pass

class Item:
    def __init__(self) -> None:
        self.name = ""
        self.amnt = 1
        self.weight = 0
        self.value = 0
        self.desc = ""
        pass
    def __repr__(self) -> str:
        pass 
    def save_json(self):
        return {"name":self.name,
                "amnt":self.amnt,
                "weight":self.weight,
                "value":self.value,
                "desc":self.desc,}
    def load_json(self, json_data):
        self.name = json_data["name"]
        self.amnt = float(json_data["amnt"])
        self.weight = float(json_data['weight'])
        self.value = float(json_data['value'])
        self.desc = json_data['desc']