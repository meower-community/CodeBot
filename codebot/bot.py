from MeowerBot import bot, __version__
from MeowerBot.context import CTX, Post, User
from MeowerBot._Commands import _Command as command
import inspect

import datetime
#calc current time

now = datetime.datetime.now()
filename = now.strftime("%d/%m/%Y-%H:%M:%S") + ".txt"



class CodeBot(bot):
    def __init__(self, debug_file):
        super.__init__(prefix="@CodeBot", debug_out=debug_file, debug=True)
        self.ignore_functions = []

        self.commands = {func.name:func for func in self.__dir__.values() if isinstance(func, command)}
        self.pages = []

    @command(name="help")
    def help(ctx, page):
        #pages are 50 lines
        if self.pages == list():
          ctx.reply("Generating Help....\n Please wait as this will take a second")
          cur_line = "'"
          curr_page = []
          self.pages = []

          i = 0
          p_s = 0
          for name ,command in self.commands.values():
            if i >= 8:
               if p_s + (len(curr_line) + 1) >= 200:
                   self.pages.append(curr_page)
                   curr_page = []
                   p_s = 0

               p_s+=len(curr_line) + 1

               curr_page.append(curr_line + "'")


               curr_line = "'"
               i = 0
               
            i+=1
            
            spec = inspect.signature(command.function)
            args = spec.parameters
            for arg in args.values():
                if arg.default is not arg.empty:
                    curr_line += f"<{arg.name}"
                else:
                    curr_line += f"<{arg.name}"
            
        if len(self.pages) < page: 
           ctx.reply(f"I only have {len(self.pages)} help pages ):")
           return
        
        c.reply("\n" + "\n".join(self.pages[page]))






        
        

