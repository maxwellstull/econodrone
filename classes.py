import json

class App():
    # Creation
    def __init__(self) -> None:
        self.servers = {}
    def add_user(self, message):
        self.servers[message.guild.id].add_user(message)
    def add_server(self, id):
        self.servers[id] = Server()
    # Save / Load
    def load_json(self):
        print("App level json load")
        fp = open("savedata.json","r")
        to_load = json.load(fp)
        for server_id, server in to_load.items():
            print("Server:", server_id)
            self.servers[server_id] = Server()
            self.servers[server_id].load_json(server)
        print("Done loading jsons")
        for i, j in self.servers.items():
            print(i, j)
    def save_json(self):
        to_save = {}
        for server_id, server in self.servers.items():
            print(server_id, server)
            to_save[server_id] = server.save_json()
        with open("savedata.json","w") as fp:
            json.dump(to_save, fp)
    # Currency
    def add(self, author, message): 
        pass 
    def remove(self, author, message):
        pass 
    def get_balance(self, author):
        pass 
    def pay_player(self, author, message):
        pass 
    # Food
    def add_ration(self, author, message):
        pass 
    def remove_ration(self, author, message):
        pass 
    # DM Comments
    def next_day(self):
        pass
    def audit(self):
        pass 
    # Misc
    def print_user(self, message):
        return self.servers[str(message.guild.id)].users[str(message.author.id)]
        

class Server():
    def __init__(self) -> None:
        
        self.users = {}
        print("\tServer object constructed")
    def load_json(self, json_data):
        print("\tServer level json load")
        for user_id, user in json_data.items():
            print("User",user_id)
            self.users[user_id] = User()
            self.users[user_id].load_json(user)
        print("\tServer level json loaded: ", self)
    def save_json(self):
        to_save = {}
        for user_id, user in self.users.items():
            to_save[user_id] = user.save_json()
        return to_save
    def add_user(self, message):
        self.users[message.author.id] = User(message.author.id, message.author.name, message.author.nick)
    def __repr__(self):
        return "User Ct: {ct}".format(ct=len(self.users))
class User():
    def __init__(self, id=0, name="", nick="") -> None:

        self.id = id 
        self.name = name
        self.nick = nick
        self.currency = Money()
        self.rations = Ration()
        print("\t\tUser object constructed.")
    def load_json(self, json_data):
        print("\t\tUser level json load")
        self.id = json_data['id']
        self.name = json_data['name']
        self.nick = json_data['nick']
        self.currency.load_json(json_data['currency'])
        self.rations.load_json(json_data['rations'])
        print("\t\tUser level json loaded: ", self)
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
        print("\t\t\tMoney object constructed")
    def __repr__(self) -> str:
        retval = "[{pl}p,{gp}g,{cu}c]".format(pl=self.plat, gp=self.gold, cu=self.copper)
        return retval 
    def save_json(self):
        return {"p":self.plat, "g":self.gold, "c":self.copper}
    def load_json(self, json_data):
        print("\t\t\tMoney level json load")
        self.copper = json_data['c']
        self.gold = json_data['g']
        self.plat = json_data['p']
        print("\t\t\tMoney level json loaded: ", self)
    
class Ration():
    def __init__(self) -> None:
        self.food = 0
        self.water = 0
        print("\t\t\tRation object constructed")
    def __repr__(self) -> str:
        retval = "[{fd} meals, {wt} gal]".format(fd=self.food,wt=self.water)
        return retval
    def save_json(self):
        return {"meals":self.food, "water":self.water}
    def load_json(self, json_data):
        print("\t\t\tRation level json load")
        self.food = json_data['meals']
        self.water = json_data['water']
        print("\t\t\tRation level json loaded: ", self)