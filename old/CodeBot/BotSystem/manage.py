"""
  File that defines and loads the bot
"""

from MeowerBot import Client
from ._handlers import InternalBot
import traceback

class DummyHandlers:
  def __init__(self, bot):
    print("You Should define Bot Handlers!!!!")
    self.bot = bot

  def on_login(self):
    print("You Should define Bot Handlers!!!!")
    pass

  def handle_pre_msg(self, *args):
    print("You Should define Bot Handlers!!!!")
    pass

def _init(debug, username, password, Commands, UnderGroundBotNetworking, Handlers):
  Bot = Client(username, password, debug=debug)

  Bot._internal_handlers = InternalBot(Bot)
  Bot.handle = Handlers(Bot, Bot._internal_handlers.send_msg)
  
  Bot.cmds = Commands(Bot, Bot._internal_handlers.send_msg)
  Bot.ubl = UnderGroundBotNetworking(Bot, Bot._internal_handlers.send_msg)
  
  Bot.callback(Bot.handle.on_login)
  Bot.callback(Bot._internal_handlers.on_raw_msg)
  Bot.callback(Bot._internal_handlers.on_raw_packet)
  return Bot

def run(username, password, cmds, BotNetwork, handlers=DummyHandlers, debug=False):
  Bot = _init(debug, username, password, cmds, BotNetwork, handlers)

  try:
    Bot.start()
  except KeyboardInterrupt:
    from sys import exit
    traceback.print_exc()
    exit()
  except:
      traceback.print_exc()
      pass

__all__ = ["run"]