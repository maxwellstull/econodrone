
class App():
    # Creation
    def __init__(self) -> None:
        self.users = {}
    def add_user(self, author):
        self.users[author.id] = User(author.id, author.name, author.nick)
    # Save / Load
    def load_json(self):
        pass
    def save_json(self):
        pass
    # Currency
    def add(self, author, message): 
        pass 
    def add_complex(self, author, message):
        pass 
    def remove(self, author, message):
        pass 
    def remove_complex(self, author, message):
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

        



class User():
    def __init__(self, id, name, nick) -> None:
        self.id = id 
        self.name = name
        self.nick = nick
        self.currency = Money()
        self.rations = Ration()
    def load_json(self):
        pass 
    def save_json(self):
        pass 

class Money():
    def __init__(self) -> None:
        self.copper = 0
        self.gold = 0
        self.plat = 0
    def __repr__(self) -> str:
        retval = "[{pl}p,{gp}g,{cu}c]".format(pl=self.plat, gp=self.gold, cu=self.copper)
        return retval 
    
class Ration():
    def __init__(self) -> None:
        self.food = 0
        self.water = 0
    def __repr__(self) -> str:
        retval = "[{fd} meals, {wt} gal]".format(fd=self.food,wt=self.water)
        return retval