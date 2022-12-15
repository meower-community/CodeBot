
import datetime
import string
import time
import uuid
from os import environ as env
from random import choice, randint

from MeowerBot import Bot, __version__
from MeowerBot.cog import Cog
from MeowerBot.command import AppCommand, command
from MeowerBot.context import CTX, Post, User
from montydb import MontyClient

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



class CommandsCog(Cog):
    def run(self, *args):
      self.bot.run(*args)
      

    def __init__(self, bot):
      self.bot = bot
      self.db = MontyClient("./db/CodeBot")
      self.pages = []
      self.admins = ["ShowierData9978"]
      Cog.__init__(self)
  

    def generate_help(self):
        self.pages = []
        page = ""
        page_size = 0

        for name in self.bot.commands:
          func = self.bot.commands[name]
          command = func["command"]
         
          current_cmd = f"{self.bot.prefix}{func.name}"
          if func["args"] is 0:
            current_cmd += f" <args: Any"
          else:
           for arg in func["arg_names"]:
              current_cmd += f" < {arg}: {func['arg_types'].get(arg, 'Any')} >"

          
          cmd_size = len(current_cmd)
          
          if page_size + cmd_size > 300:
            self.pages.append(page)
            page = ""
          page += f"{current_cmd}\n"
          page_size += cmd_size+1




        

            
            


    @command(name="help", args=1)
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

    @command(args=1)
    def info(self, ctx:CTX, about):
      if about == "Bot":
           ctx.send_msg(f"""
    Bot Info:
  Owned by @ShowierData9978
  Bot Lib: MeowerBot.py {__version__}
  Source Code: 
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

    @command(args=1)
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
          email += choice(email_names)

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

    @command(args=2)
    def send_coins(self, ctx, user, coins):
      if not self.db.CodeBot.users.find_one({"username":ctx.user.username}):
        self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":ctx.user.username, "coins": 0, "collectables": [], "t": 0})

      if not self.db.CodeBot.users.find_one({"username":user}):
        self.db.CodeBot.users.insert_one({"_id":uuid.uuid4(), "username":user, "coins": 0, "collectables": [], "t": 0})

      sender = self.db.CodeBot.users.find_one(
          {"username":ctx.user.username}
        )
      assert sender is not None

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

      ctx.reply("sent the coins!")

    @command()
    def beg(self, ctx):
        if not self.db.CodeBot.users.find_one({"username":ctx.user.username}):
          self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":ctx.user.username, "coins": 0, "collectables": [], "t": 0})

        usr = self.db.CodeBot.users.find_one({"username":ctx.user.username})
        assert usr is not None
        
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
        assert user is not None
        ctx.send_msg(
                f"@{ctx.user.username} user {usr} has {user['coins']} coins!")

    @command()
    def inventory(self, ctx):
        if not self.db.CodeBot.users.find_one({"username":ctx.user.username}):
          self.db.CodeBot.users.insert_one({"_id":uuid.uuid4().hex, "username":ctx.user.username, "coins": 0, "collectables": [], "t": 0})

        usr = self.db.CodeBot.users.find_one({'username':ctx.user.username})
        assert usr is not None

        ctx.send_msg(
            f"@{ctx.user.username} you have the the items\n" +
            ", \n".join(usr["collectables"])

        )

    @command()
    def shop(self, ctx):
        msg = ""
        for n, v in Shop.items():
            msg += f"name: {n}, value: {v} coins \n"
        ctx.send_msg(msg)

    @command(args=1)
    def buy(self, ctx, item):
        if not item in Shop.keys():
            ctx.send_msg(
                f"@{ctx.user.username} The item of '{item}' was not found in the shop"
                )
            return

        usr = self.db.CodeBot.users.find_one({'username':ctx.user.username})
        assert usr is not None
        if not Shop[item] <= usr["coins"]:
            ctx.send_msg(
                f"@{ctx.user.username} You do not have enough coins for {item}")


        self.db.CodeBot.users.update_one(
          {"username":ctx.user.username},
          {"$push":{"collectables":[item]}, "$set": {"coins": usr["coins"] - Shop[item]}
        })

    @command(args=1)
    def ban(self, ctx, person):
        if not ctx.user.username in self.admins:
            ctx.send_msg(
                f"@{ctx.user.username} you dont have permision to ban from this bot.")
            return
        self.db.CodeBot.bans.insert_one({'_id':uuid.uuid4(), "username": person.replace("@", "")})
        ctx.send_msg(f"Banned @{person} from this bot")

    @command(args=1)
    def unban(self, ctx, person):
        if not ctx.user.username in self.admins:
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
        if not ctx.user.username in self.admins:
            ctx.send_msg(f"@{ctx.user.username} you dont have permision to add a todo",
                          )
            return

        with open("todo.txt", "a") as f:
            f.write(" ".join(args) + "\n")

        ctx.send_msg("Added the todo to `todo.txt`")

    @command(args=1)
    def todo(self, ctx, line):
        with open("todo.txt", "r") as f:
            lines = f.readlines()
            if len(lines) < int(line) - 1:
                ctx.send_msg(f"There is only {len(lines)} todo(s)")
                return
            ctx.send_msg(lines[int(line) - 1])

    @command()
    def remove_todo(self, ctx, *args):
        if not ctx.user.username in self.admins:
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

    @command()
    def dm(self, *args):
        self.db.CodeBot.dms.insert_one({"_id":uuid.uuid4().hex, 'username':args[0], 'message':args[1]})
