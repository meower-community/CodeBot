from typing import Optional, Any

import pathlib
from os import environ as env

from cog import CommandsCog
from MeowerBot import Bot, __version__
import traceback
from dotenv import load_dotenv

load_dotenv(override=True)

import pymongo


class BotMngr(Bot):
  """
         func overides
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.db:Any = None

def ulist(*users, **kwargs):
        bot: BotMngr = kwargs['bot']

        if not bot.logger_in: return
        assert bot is not None
        for user in users:
          dm = bot.db.CodeBot.dms.find_one({'username': user})
          if dm:
            bot.send_msg(f"@{dm['username']}, @{dm['sender']} sent you a DM\n\n{dm['message']}")
            bot.db.CodeBot.dms.delete_one({"username": user})
            return

def error(err, **kwargs):
   traceback.print_exception(err)




if __name__ == "__main__":
    import logging
    
    
    #to a file
    logging.basicConfig(filename='logs/codebot.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    #logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    bot = BotMngr(prefix="@CodeBot ", autoreload=0)
    bot.callback(ulist)

    cog = CommandsCog(bot)
    bot.register_cog(cog)

    cog.generate_help()
    bot.run("CodeBot", env['password'])






