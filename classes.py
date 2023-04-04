import json

class App():
    # Creation
    def __init__(self) -> None:
        self.users = {}
    def add_user(self, author):
        self.users[author.id] = User(author.id, author.name, author.nick)
    # Save / Load
    def load_json(self):
        fp = open("savedata.json","r")
        to_load = json.load(fp)
        for user_id, user in to_load.items():
            self.users[user_id] = User().load_json(user)

    def save_json(self):
        to_save = {}
        for user_id, user in self.users.items():
            to_save[user_id] = user.save_json()
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
    def print_user(self, id):
        print(self.users[id])
        



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
        self.currency = Money().load_json(json_data['currency'])
        self.rations = Ration().load_json(json_data['rations'])
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