import time
import traceback
from os import environ as env
from os import system as run
from random import randint, choice
from sys import argv
from threading import Thread
import uuid
from MeowerBot import Client
import string

import math
import datetime
Shop = {
    "Rare_Coin": 50,
    "24k_gold": 400,
    "Me_Upgradeing_MeowerBot": 4000,
    "DBReset": 5000000,
    "Refactoring": 10000,
}

group_chats = [
    "FurryGang", "DiscordIsBetter", "Discord_General", "Discord_Offtopic",
    "BotHell", "HomeV2", "school", "ShowierData9978", "Bots", "banned",
    "underage"
]

email_names = [
    "hak", "bob", "meowerbot", "bob_bot", "meower", "meowy",
    "showierdata.tech", "butt", "underage", "excitement", "brown",
    "incongruous", "prospect", "exposure", "unfortunate", "bundle",
    "background", "wave", "conviction", "earthflax", "cane", "hospitality",
    "accompany", "priority", "archive", "substitute", "coal", "beneficiary",
    "crowd", "addition", "magnetic", "obligation", "classroom", "obscure",
    "electron", "tempt", "disagree", "holiday", "series"
]

  
    


class Commands:

    def __init__(self, bot, send_msg):
        self.bot = bot
        self.send_msg = send_msg
        self.db = self.bot.db
  
    def info(self, cmd, *args, raw={}):
        if cmd == "bot":
            self.send_msg(
                """
Bot Info:
  Owned by @ShowierData9978
  Bot Lib: MeowerBot.py 1.4.1 (cl3)
  Hosting & Src: replit @showierdata9971/ShowiersMeowerBot
    """,
                raw,
            )
        elif cmd == "website":
            self.send_msg("https://showierdata.tech", raw)
        elif cmd == "Webhooks":
            self.send_msg(
                """
webhooks is a bot that is hosted by @ShowierData9978 on his RPI.
You can send a message through it with the URL 
    meower-webhook.showierdata.tech/post/home

    @ShowierData9978 personaly uses reqbin.com to send POST Requests.

    The required args are (in json)
      post:str    
      """,
                raw,
            )

    def help(self, *args, raw={}):
        try:
            page = args[0]
        except IndexError:
            page = 1

        if int(page) == 1:
            self.send_msg(
                """
'help <num>
'info bot'
'info website'
'todo <line>'
'help 2'
  """,
                raw,
            )
        elif int(page) == 2:
            self.send_msg(
                """
'info Webhooks'
'mimic'
'hack User'
'beg'
'help 3'
    """,
                raw,
            )
        elif int(page) == 3:
            self.send_msg(
                """
'bal'
'send_coins <user> <ammount>''
          """,
                raw,
            )

        else:
            self.send_msg(f"@{raw['u']} I do not have that index", raw)

    def mimic(self, *args, raw={}):
        if False and not raw['u'] == 'ShowierData9978':
            self.send_msg(
                "Disabled",
                raw,
            )
            return

        self.send_msg(" ".join(*args), raw)

    def hack(self, user, *args, raw={}):
        if user == env['Username']:
            self.send_msg("Im Not hacking myself, RUDE.", raw)
            return

        self.send_msg(f"toltaly hacking @{user}", raw)
        time.sleep(randint(3, 5))

        #random chance to fail
        if randint(1, 10000) > 10000 - 1:
            self.send_msg(f"I Have failed to hack @{user}", raw)
            return

        self.send_msg(f"Got access to @{user}`s Meower Account...", raw)
        time.sleep(randint(1, 5))

        email = ""
        for i in range(randint(1, 5)):
          email + choice(email_names)

        email+="@"+choice(email_names)+"."+choice([
            "com", "org", "net", "edu", "gov", "mil", "biz", "info", "name"])
      
        self.send_msg(f"Email: {email}", raw)

        time.sleep(randint(0, 2))
      
        password = ''
        for _ in range(0, randint(12, 16)):
            password += choice(string.printable + string.digits +
                               string.punctuation)

        self.send_msg(f"changeing password....\n Password set to {password}",
                      raw)
        time.sleep(randint(2, 4))

        chats = ''
        for _ in range(randint(0, len(group_chats))):
            chats += choice(group_chats) + '\n'

        if user == 'm' or user.startswith("MDWalters"):
            chats += "AntiFurryGang\n"
        self.send_msg(f"leaking group chats... \n {chats}", raw)

        #80% chance to send reporting to meower
        if randint(1, 100) > 80:
            self.send_msg(f"Reporting @{user} to meower.....", raw)

        time.sleep(randint(1, 2))

        # last ip....
        if randint(1, 100) > 80:
            ip = f"{round(randint(1, 255))}.{round(randint(1, 255))}.{round(randint(1, 255))}.{round(randint(1, 255))}"
            self.send_msg(f"Last IP: {ip}", raw)

        time.sleep(randint(0, 2))

        time.sleep(randint(1, 4))
        self.send_msg(f"Finished Hacking @{user}`s Account", raw)

    def send_coins(self, user, coins, *args, raw={}):
      if not self.db.CodeBot.users.find_one({"username":raw['u']}):
        self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":raw['u'], "coins": 0, "collectables": [], "t": 0})

      if not self.db.CodeBot.users.find_one({"username":user}):
        self.db.CodeBot.users.insert_one({"_id":uuid.uuid4(), "username":user, "coins": 0, "collectables": [], "t": 0})

      sender = self.db.CodeBot.users.find_one(
          {"username":raw['u']}
        )
      recever = self.db.CodeBot.users.find_one({"username":user})
                                         
      if not sender['coins'] > int(coins):
        self.send_msg(f"{raw['u']} Im sorry, but you dont have enough coins", raw)
        return 
        
      self.db.CodeBot.users.update_one(
        {"username":raw['u']}, 
        {
          "$set":{
            "coins":sender['coins'] - int(coins)
          }
        }
      )
      
      self.db.CodeBot.users.update_one(
        {"username":raw['u']}, 
        {
          "$set":{
            "coins":sender['coins'] + int(coins)
          }
        }
      )

      self.send_msg(f"@{raw['u']} sent the coins!", raw)
    
  
    def beg(self, *args, raw={}):
        if not self.db.CodeBot.users.find_one({"username":raw['u']}):
          self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":raw['u'], "coins": 0, "collectables": [], "t": 0})

        usr = self.db.CodeBot.users.find_one({"username":raw['u']})
        
      
        if not time.time() - usr["t"] >= 60 * 3:  # 3 minutes
            self.send_msg(
                f"@{raw['u']} You cant run this command yet (cooldown)\n you have " + str(datetime.timedelta(seconds=round((60*3-(time.time() - usr["t"]))))) + " left", raw)
            return

        if randint(0, 20) != 1:
            amm = randint(1, 30)

            self.db.CodeBot.users.update_one({"username":raw['u']}, {"$set":{"coins":usr["coins"] + amm}})
        else:

            amm = randint(400, 1000)
            self.db.CodeBot.users.update_one({"username":raw['u']}, {"$set":{"coins":usr["coins"] + amm}})


              
        self.db.CodeBot.users.update_one({"username":raw['u']}, {"$set":{"t":time.time()}})
        self.send_msg(f"@{raw['u']} You got {amm} coins!", raw)

    def bal(self, *args, raw={}):
        try:
          usr = args[0]
        except:
          usr = raw['u']

      
        if not self.db.CodeBot.users.find_one({"username":usr}):
          self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":raw['u'], "coins": 0, "collectables": [], "t": 0})

        user = self.db.CodeBot.users.find_one({"username":usr})
      
        self.send_msg(
                f"@{raw['u']} user {usr} has {user['coins']} coins!", raw)

    def inventory(self, *args, raw={}):
        if not self.db.CodeBot.users.find_one({"username":raw['u']}):
          self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":raw['u'], "coins": 0, "collectables": [], "t": 0})

        usr = self.db.CodeBot.users.find_one({'username':raw['u']}) 
        
        self.send_msg(
            f"@{raw['u']} you have the the items\n" +
            ", \n".join(usr["collectables"]),
            raw,
        )

    def shop(self, *args, raw={}):
        msg = ""
        for n, v in Shop.items():
            msg + f"name: {n}, value: {v} coins \n"
        self.send_msg(msg, raw)

    def buy(self, item, *args, raw={}):
        if not item in Shop.keys():
            self.send_msg(
                f"@{raw['u']} The item of '{item}' was not found in the shop",
                raw)
            return
        
        usr = self.db.CodeBot.users.find_one({'username':raw['u']})
        if not Shop[item] <= usr["coins"]:
            self.send_msg(
                f"@{raw['u']} You do not have enough coins for {item}", raw)

        
        self.db.CodeBot.users.update_one(
          {"username":raw["u"]}, 
          {"$push":{"collectables":[item]}, "$set": {"coins": usr["coins"] - Shop[item]}
        })
      
    def ban(self, person, raw={}):
        if not raw["u"] == "ShowierData9978":
            self.send_msg(
                f"@{raw['u']} you dont have permision to ban from this bot.",
                raw)
            return
        self.db.CodeBot.bans.insert_one({'_id':uuid.uuid4(), "username": person.replace("@", "")})
        self.send_msg(f"Banned @{person} from this bot", raw)

    def unban(self, person, raw={}):
        if not raw["u"] == "ShowierData9978":
            self.send_msg(
                f"@{raw['u']} you dont have permision to unban from this bot.",
                raw)
            return

        if not person.replace("@", "") in self.db.CodeBot.bans.find_many({}):
            self.send_msg(f"@{raw['u']} @{person} is not banend", raw)
            return

        self.db.CodeBot.bans.delete_one({"username":person.replace("@", "")})
        
        self.send_msg(f"unbanned @{person} from this bot", raw)

    def add_todo(self, *args, raw={}):  # *args is the todo
        if not raw["u"] == "ShowierData9978":
            self.send_msg(f"@{raw['u']} you dont have permision to add a todo",
                          raw)
            return

        with open("todo.txt", "a") as f:
            f.write(" ".join(args) + "\n")

        self.send_msg("Added the todo to `todo.txt`", raw)

    def todo(self, line, *args, raw={}):
        with open("todo.txt", "r") as f:
            lines = f.readlines()
            if len(lines) < int(line) - 1:
                self.send_msg(f"There is only {len(lines)} todo(s)", raw)
                return
            self.send_msg(lines[int(line) - 1], raw)

    def remove_todo(self, *args, raw={}):
        if not raw["u"] == "ShowierData9978":
            self.send_msg(
                f"@{raw['u']} you dont have permision to remove a todo", raw)
            return

        with open("todo.txt", "r+") as f:
            d = f.readlines()
            f.seek(0)
            f.truncate()
            for i in d:
                if i.strip("\n") != " ".join(args):
                    f.write(i)
        self.send_msg("removed todo", raw)

    def get_owner_inp(self, *args, raw={}):
        if not len(argv) >= 2:
            self.send_msg("Owner is not here right now", raw)
            return

        def _():
          while True:
            inp = input("\n?> ").strip()

            #change the chat.
            imp_args = inp.split(" ")

            if 'chat' in imp_args:
              raw['post_origin'] = " ".join(imp_args[imp_args.index('chat')+1:imp_args.index('end')])
              imp_args.remove("chat")
              for a in raw['post_origin'].split(" "):
                imp_args.remove(a)
              imp_args.remove("end")
              inp = " ".join(imp_args)
              
              print(raw['post_origin'])
            if 'ulist' in inp:
              print(self.bot._wss.statedata['ulist']['usernames'])
              self.bot.inp_mode = True
              self.send_msg("Owner Got ulist", raw)
            elif 'split' in inp:
                cmds = inp.split("split")
                for cmd in cmds:
                  self.bot.inp_mode = True
                  self.send_msg(cmd.strip(), raw)
                  time.sleep(0.5)
            else:
              self.send_msg(inp, raw)
            self.bot.inp_mode = True

        Thread(target=_).start()

    def dm(self, *args, raw={}):
        self.db.CodeBot.dms.insert_one({"_id":uuid.uuid4().hex, 'username':args[0], 'message':args[1]})

__all__ = ["Commands"]
