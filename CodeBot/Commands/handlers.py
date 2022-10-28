from os import environ as env
from os import system as run
from sys import argv
from replit import db

from json import loads
from montydb import MontyClient, set_storage


set_storage("./db/CodeBot", cache_modified=0) 

class Handlers:
    def __init__(self, bot, send_msg):
        self.bot = bot
        self.bot.db =  MontyClient("./db/CodeBot")
        self.db = self.bot.db
        self.send_msg = send_msg
        bot.inp_mode = False
        bot.ulist = []

    def handle_pre_msg(self, args, msg, bot):
        if msg["u"] == env["Username"] and not self.bot.inp_mode:
            return False

        if not args[0] == "@CodeBot":

            return False

        self.bot.inp_mode = False

        if self.db.CodeBot.bans.find_one({"username": msg['u']}):
            self.send_msg(
                f"Sad @{msg['u']} is banned from this bot, and is trying to use it.",
                msg,
            )
            return False

        return True

    def on_login(self):

        self.bot.send_msg(
            "Prefix: '@CodeBot '\n Bot info: @CodeBot info bot\n For Help do 'help 1'"
        )
        if len(argv) >= 2:
            self.bot.inp_mode = True
            self.bot.send_msg("@CodeBot get_owner_inp " + input("> "))
            


__all__ = ["Handlers"]
