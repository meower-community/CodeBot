from typing import Optional, Any

import pathlib
from os import environ as env

from cog import CommandsCog
from MeowerBot import Bot, __version__
from montydb import set_storage

set_storage("./db/CodeBot", cache_modified=0)




class BotMngr(Bot):
  """
         func overides
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.db:Any = None

def ulist(users, **kwargs):
        bot = kwargs['bot']

        if bot.logging_in: return
        assert bot is not None
        for user in users:
          dm = bot.db.CodeBot.dms.find_one({'username': user})
          if dm:
            bot.send_msg(f"@{dm['username']}, @{dm['sender']} send you a DM\n so here it is!:\n\t{dm['message']}")
            bot.db.CodeBot.dms.delete_one({"username": user})
            return



if __name__ == "__main__":
    import logging
    
    
    #to a file
    logging.basicConfig(filename='logs/codebot.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    bot = BotMngr(prefix="@CodeBot ")
    bot.callback(ulist)

    cog = CommandsCog(bot)
    bot.register_cog(cog)

    cog.generate_help()
    bot.run("CodeBot", env['password'])






