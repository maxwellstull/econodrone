import json

class App():
    # Creation
    def __init__(self) -> None:
        self.servers = {}
    def add_user(self, message):
        self.servers[str(message.guild.id)].add_user(message)
    def add_server(self, id):
        self.servers[id] = Server()
    # Save / Load
    def load_json(self):
        fp = open("savedata.json","r")
        to_load = json.load(fp)
        for server_id, server in to_load.items():
            self.servers[server_id] = Server()
            self.servers[server_id].load_json(server)
        print("Json Loaded")
    def save_json(self):
        to_save = {}
        for server_id, server in self.servers.items():
            print(server_id, server)
            to_save[server_id] = server.save_json()
        with open("savedata.json","w") as fp:
            json.dump(to_save, fp)
    # Currency
    def add(self, message, payload): 
        self.servers[str(message.guild.id)].compute(message, payload, 1)
    def remove(self, message, payload):
        self.servers[str(message.guild.id)].compute(message, payload, -1)
    # Food
    def add_ration(self, message, payload):
        self.servers[str(message.guild.id)].compute_ration(message, payload, 1)
    def remove_ration(self, message, payload):
        self.servers[str(message.guild.id)].compute_ration(message, payload, -1)
    def add_water(self, message, payload):
        self.servers[str(message.guild.id)].compute_water(message, payload, 1)
    def drink_water(self, message, payload):
        self.servers[str(message.guild.id)].compute_water(message, payload, -1)
    # DM Comments
    def next_day(self,message):
        for user in self.servers[str(message.guild.id)].users:
            user.rations.food = user.rations.food - 1
            user.rations.water = user.rations.water - 1
    def audit(self, message):
        retval = ""
        for _id, user in self.servers[str(message.guild.id)].users.items():
            retval += str(user)
            retval += "\n\n"
        return retval
    # Misc
    def print_user(self, message):
        return self.servers[str(message.guild.id)].users[str(message.author.id)]
        

class Server():
    def __init__(self) -> None:
        self.users = {}
    def load_json(self, json_data):
        for user_id, user in json_data.items():
            self.users[user_id] = User()
            self.users[user_id].load_json(user)
    def save_json(self):
        to_save = {}
        for user_id, user in self.users.items():
            to_save[user_id] = user.save_json()
        return to_save
    def add_user(self, message):
        self.users[message.author.id] = User(message.author.id, message.author.name, message.author.nick)
    def __repr__(self):
        return "User Ct: {ct}".format(ct=len(self.users))
    def compute(self, message, payload, modifier):
        print(payload[1:])
        for i in range(1, len(payload), 2):
            coin_type = payload[i].replace("--","")
            coin_amnt = int(payload[i+1])
            match coin_type:
                case "p":
                    self.users[str(message.author.id)].currency.plat = self.users[str(message.author.id)].currency.plat + modifier*coin_amnt
                case "g":
                    self.users[str(message.author.id)].currency.gold = self.users[str(message.author.id)].currency.gold + modifier*coin_amnt
                case "c":
                    self.users[str(message.author.id)].currency.copper = self.users[str(message.author.id)].currency.copper + modifier*coin_amnt
    def compute_ration(self, message, payload, modifier):
        self.users[str(message.author.id)].rations.food = self.users[str(message.author.id)].rations.food + modifier*int(payload[1])
    def compute_water(self, message, payload, modifier):
        self.users[str(message.author.id)].rations.water = self.users[str(message.author.id)].rations.water + modifier*int(payload[1])

            

class User():
    def __init__(self, id=0, name="", nick="") -> None:
        self.id = id 
        self.name = name
        self.nick = nick
        self.currency = Money()
        self.rations = Ration()
    def load_json(self, json_data):
        self.id = json_data['id']
        self.name = json_data['name']
        self.nick = json_data['nick']
        self.currency.load_json(json_data['currency'])
        self.rations.load_json(json_data['rations'])
    def save_json(self):
        return {"id":self.id, "name":self.name, "nick":self.nick, "currency":self.currency.save_json(), "rations":self.rations.save_json()}
    def __repr__(self) -> str:
        return """
        Name: {nm}
        Nick: {nk}
            Money: {m}
            Ration: {r}
        """.format(nm = self.name, nk=self.nick, m=str(self.currency), r=str(self.rations))

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
        self.water = 0
    def __repr__(self) -> str:
        retval = "[{fd} meals, {wt} gal]".format(fd=self.food,wt=self.water)
        return retval
    def save_json(self):
        return {"meals":self.food, "water":self.water}
    def load_json(self, json_data):
        self.food = json_data['meals']
        self.water = json_data['water']