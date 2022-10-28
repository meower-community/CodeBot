from .BotSystem import run

from .bots.networking import  UnderGroundBotNetworking
from .Commands.handlers import Handlers
from .Commands.commands import Commands

from os import environ as env
import traceback

def start_code_bot():
  try:
    run(
      env["Username"], 
      env["Password"],  
      Commands, 
      UnderGroundBotNetworking,
      Handlers,
      debug=False
    )
  except Exception as e:
    traceback.print_exc()

  finally:
    print("Bot is shutting down")
    
    from sys import exit
    exit(0)
    
    