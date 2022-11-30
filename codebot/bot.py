from MeowerBot import Bot, __version__
from MeowerBot.context import CTX, Post, User
from MeowerBot._Commands import _Command
import inspect

import datetime

from os import environ as env 
import shlex
from random import randint, choice
import time
import string
import uuid
#calc current time

import traceback

from montydb import MontyClient, set_storage

set_storage("./db/CodeBot", cache_modified=0) 


now = datetime.datetime.now()
filename = now.strftime("%d-%m-%Y_%H:%M:%S") + ".txt"

with open("logs/" + filename, "w"):
	pass #create the file
	

#constents

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

  
global traceback.print_exc




class command(_Command):
  def run_cmd(self, *args, ctx):
    self.func(self.bot.cmds, ctx, *args)


  def __call__(self, func):
    self.func = func
    if self.name is None:
        self.name = self.func.__name__
    return self.run_cmd


class BotMngr(Bot):
  """
         func overides
  """
    
  def __init__(self, bot, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.cmds = bot
        
        
  def run_command(self, message):
      args = shlex.split(str(message.data))

      print("cmd")
      try:
        self.commands[args[0]].run_cmd(args[1:], message.ctx)
      except Exception as e:
        if self.bot.debug:
           traceback.print_exc()
        self.run_cb("error", args=(e,))
            


class CodeBot:
    def run(self, *args):
      self.bot.run(*args)

    def error(self, e, *args, bot=None):
       traceback.print_exc()

    def message(msg, bot=""):
      if msg.ctx.user.username == self.bot.username: return
      
      if msg.user.username == "Discord":
        msg.user.username = msg.data.split(": ")[0]
        msg.data = msg.data.split(": ")[1]
      
      if not msg.ctx.message.data.startswith(self.bot.prefix): return
      message.data = message.data.split(self.bot.prefix, 1)[1]
      bot.run_command(msg)
	
    def __init__(self, debug_file):
        self.bot = BotMngr(self, prefix="@CodeBot", debug=True, debug_out=debug_file)
        self.ignore_functions = []

        self.bot.callback('error', self.error)
        self.bot.callback("message", self.message)
			
        self.commands = {func.name:func for func in self.__dict__.values() if isinstance(func, command)}
        
        self.pages = []


        self.db =  MontyClient("./db/CodeBot")

        self.admins = ["ShowierData9978"]

        cur_line = "'"
        curr_page = []
        self.pages = []
            
        i = 0
        p_s = 0
        for name , Command in self.commands.values():
          Command._bot = self.bot
          if i >= 8:
            if p_s + (len(cur_line) + 1) >= 200:
              self.pages.append(curr_page)
              curr_page = []
              p_s = 0

              p_s+=len(cur_line) + 1

            curr_page.append(cur_line + "'")


            curr_line = "'"
            i = 0
               
          i+=1
            
          spec = inspect.signature(Command.function)
          args = spec.parameters
          cur_line += f"{self.prefix} {name}"
          if 'self' in args: args = args[1:]
          args = args[1:] #context
                        
          for arg in args.values():
            if arg.default is not arg.empty:
              curr_line += f"<{arg.name}"
            else:
              curr_line += f"<{arg.name}"

    @command(name="help")
    def help(self, ctx, page):
    
        if len(self.pages) < page: 
           ctx.reply(f"I only have {len(self.pages)} help pages ):")
           return
        
        ctx.reply("\n" + "\n".join(self.pages[page]))

    @command()
    def mimic(self, ctx:CTX, *args):
      if not ctx.user.username in self.admins:
        ctx.reply("This Command Is Bot admin locked ):")
        return
      ctx.send_msg(" ".join(args))
    
    @command()
    def info(self, ctx:CTX, about):
      if about == "Bot":
           ctx.send_msg("""
    Bot Info:
  Owned by @ShowierData9978
  Bot Lib: MeowerBot.py 1.4.1 (cl3)
  Hosting & Src: replit @showierdata9971/ShowiersMeowerBot
            """)
      elif about == "website":
         ctx.send_msg("https://showierdata.tech")
      elif about.lower() == "Webhooks":
        ctx.send_msg("""
        webhooks is a bot that is hosted by @ShowierData9978 on his RPI.
    You can send a message through it with the URL 
    https://webhooks.meower.org/post/home

    @ShowierData9978 personaly uses reqbin.com to send POST Requests.

    The required args are (in json)
      post:str
        """)
    @command()
    def hack(self, ctx:CTX, user):
        if user == env['Username']:
            ctx.send_msg("Im Not hacking myself, RUDE.")
            return

        ctx.send_msg(f"toltaly hacking @{user}")
        time.sleep(randint(3, 5))

        #random chance to fail
        if randint(1, 10000) > 10000 - 1:
            ctx.send_msg(f"I Have failed to hack @{user}")
            return

        ctx.send_msg(f"Got access to @{user}`s Meower Account...")
        time.sleep(randint(1, 5))

        email = ""
        for i in range(randint(1, 5)):
          email + choice(email_names)

        email+="@"+choice(email_names)+"."+choice([
            "com", "org", "net", "edu", "gov", "mil", "biz", "info", "name"])
      
        ctx.send_msg(f"Email: {email}")

        time.sleep(randint(0, 2))
      
        password = ''
        for _ in range(0, randint(12, 16)):
            password += choice(string.printable + string.digits +
                               string.punctuation)

        ctx.send_msg(f"changeing password....\n Password set to {password}",
                     )
        time.sleep(randint(2, 4))

        chats = ''
        for _ in range(randint(0, len(group_chats))):
            chats += choice(group_chats) + '\n'

        if user == 'm' or user.startswith("MDWalters"):
            chats += "AntiFurryGang\n"
        ctx.send_msg(f"leaking group chats... \n {chats}")

        #80% chance to send reporting to meower
        if randint(1, 100) > 80:
            ctx.send_msg(f"Reporting @{user} to meower.....")

        time.sleep(randint(1, 2))

        # last ip....
        if randint(1, 100) > 80:
            ip = f"{round(randint(1, 255))}.{round(randint(1, 255))}.{round(randint(1, 255))}.{round(randint(1, 255))}"
            ctx.send_msg(f"Last IP: {ip}")

        time.sleep(randint(0, 2))

        time.sleep(randint(1, 4))
        ctx.send_msg(f"Finished Hacking @{user}`s Account")

    @command()
    def send_coins(self, ctx, user, coins):
      if not self.db.CodeBot.users.find_one({"username":ctx.user.username}):
        self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":ctx.user.username, "coins": 0, "collectables": [], "t": 0})

      if not self.db.CodeBot.users.find_one({"username":user}):
        self.db.CodeBot.users.insert_one({"_id":uuid.uuid4(), "username":user, "coins": 0, "collectables": [], "t": 0})

      sender = self.db.CodeBot.users.find_one(
          {"username":ctx.user.username}
        )
      recever = self.db.CodeBot.users.find_one({"username":user})
                                         
      if not sender['coins'] > int(coins):
        ctx.reply("Im sorry, but you dont have enough coins")
        return 
        
      self.db.CodeBot.users.update_one(
        {"username":ctx.user.username}, 
        {
          "$set":{
            "coins":sender['coins'] - int(coins)
          }
        }
      )
      
      self.db.CodeBot.users.update_one(
        {"username":ctx.user.username}, 
        {
          "$set":{
            "coins":sender['coins'] + int(coins)
          }
        }
      )

      self.reply("sent the coins!")
    
    @command
    def beg(self, ctx):
        if not self.db.CodeBot.users.find_one({"username":ctx.user.username}):
          self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":ctx.user.username, "coins": 0, "collectables": [], "t": 0})

        usr = self.db.CodeBot.users.find_one({"username":ctx.user.username})
        
      
        if not time.time() - usr["t"] >= 60 * 3:  # 3 minutes
            ctx.send_msg(
                f"@{ctx.user.username} You cant run this command yet (cooldown)\n you have " + str(datetime.timedelta(seconds=round((60*3-(time.time() - usr["t"]))))) + " left")
            return

        if randint(0, 20) != 1:
            amm = randint(1, 30)

            self.db.CodeBot.users.update_one({"username":ctx.user.username}, {"$set":{"coins":usr["coins"] + amm}})
        else:

            amm = randint(400, 1000)
            self.db.CodeBot.users.update_one({"username":ctx.user.username}, {"$set":{"coins":usr["coins"] + amm}})


              
        self.db.CodeBot.users.update_one({"username":ctx.user.username}, {"$set":{"t":time.time()}})
        ctx.send_msg(f"@{ctx.user.username} You got {amm} coins!")

    @command()
    def bal(self, ctx, *args):
        try:
          usr = args[0]
        except:
          usr = ctx.user.username

      
        if not self.db.CodeBot.users.find_one({"username":usr}):
          self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":ctx.user.username, "coins": 0, "collectables": [], "t": 0})

        user = self.db.CodeBot.users.find_one({"username":usr})
      
        ctx.send_msg(
                f"@{ctx.user.username} user {usr} has {user['coins']} coins!")

    @command()
    def inventory(self, ctx):
        if not self.db.CodeBot.users.find_one({"username":ctx.user.username}):
          self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":ctx.user.username, "coins": 0, "collectables": [], "t": 0})

        usr = self.db.CodeBot.users.find_one({'username':ctx.user.username}) 
        
        ctx.send_msg(
            f"@{ctx.user.username} you have the the items\n" +
            ", \n".join(usr["collectables"])
            
        )

    @command()
    def shop(self, ctx):
        msg = ""
        for n, v in Shop.items():
            msg + f"name: {n}, value: {v} coins \n"
        ctx.send_msg(msg)

    def buy(self, ctx, item):
        if not item in Shop.keys():
            ctx.send_msg(
                f"@{ctx.user.username} The item of '{item}' was not found in the shop"
                )
            return
        
        usr = self.db.CodeBot.users.find_one({'username':ctx.user.username})
        if not Shop[item] <= usr["coins"]:
            ctx.send_msg(
                f"@{ctx.user.username} You do not have enough coins for {item}")

        
        self.db.CodeBot.users.update_one(
          {"username":ctx.user.username}, 
          {"$push":{"collectables":[item]}, "$set": {"coins": usr["coins"] - Shop[item]}
        })

    @command()
    def ban(self, ctx, person):
        if not ctx.user.username == "ShowierData9978":
            ctx.send_msg(
                f"@{ctx.user.username} you dont have permision to ban from this bot.",
                raw)
            return
        self.db.CodeBot.bans.insert_one({'_id':uuid.uuid4(), "username": person.replace("@", "")})
        ctx.send_msg(f"Banned @{person} from this bot")

    @command()
    def unban(self, ctx, person):
        if not ctx.user.username == "ShowierData9978":
            ctx.send_msg(
                f"@{ctx.user.username} you dont have permision to unban from this bot.",
                )
            return

        if not person.replace("@", "") in self.db.CodeBot.bans.find_many({}):
            ctx.send_msg(f"@{ctx.user.username} @{person} is not banend")
            return

        self.db.CodeBot.bans.delete_one({"username":person.replace("@", "")})
        
        ctx.send_msg(f"unbanned @{person} from this bot")

    @command()
    def add_todo(self, ctx, *args):  # *args is the todo
        if not ctx.user.username == "ShowierData9978":
            ctx.send_msg(f"@{ctx.user.username} you dont have permision to add a todo",
                          )
            return

        with open("todo.txt", "a") as f:
            f.write(" ".join(args) + "\n")

        ctx.send_msg("Added the todo to `todo.txt`")

    @command()
    def todo(self, ctx, line):
        with open("todo.txt", "r") as f:
            lines = f.readlines()
            if len(lines) < int(line) - 1:
                ctx.send_msg(f"There is only {len(lines)} todo(s)")
                return
            ctx.send_msg(lines[int(line) - 1])

    @command()
    def remove_todo(self, ctx, *args):
        if not ctx.user.username == "ShowierData9978":
            ctx.send_msg(
                f"@{ctx.user.username} you dont have permision to remove a todo")
            return

        with open("todo.txt", "r+") as f:
            d = f.readlines()
            f.seek(0)
            f.truncate()
            for i in d:
                if i.strip("\n") != " ".join(args):
                    f.write(i)
        ctx.send_msg("removed todo")

    def dm(self, *args):
        self.db.CodeBot.dms.insert_one({"_id":uuid.uuid4().hex, 'username':args[0], 'message':args[1]})

if __name__ == "__main__":
  with open("logs/" + filename, 'a') as f:
        
    bot = CodeBot(f)
    bot.run(env['Username'], env['Password'])



        
        

