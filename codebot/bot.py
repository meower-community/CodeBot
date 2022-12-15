import datetime
import pathlib
from os import environ as env

from cog import CommandsCog
from MeowerBot import Bot, __version__
from montydb import set_storage

set_storage("./db/CodeBot", cache_modified=0)


now = datetime.datetime.now()

path = pathlib.Path("logs/" +  now.strftime("%d-%m-%y"))
filename = now.strftime("%H:%M:%S") + ".log"

path.mkdir(parents=True)
file = path / filename

class BotMngr(Bot):
  """
         func overides
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


if __name__ == "__main__":
  with file.open("a") as f:

    bot = BotMngr(debug=True, debug_file=f, prefix="@CodeBot ")

    cog = CommandsCog(bot)
    bot.register_cog(cog)

    cog.generate_help()
    bot.run(env['Username'], env['Password'])






