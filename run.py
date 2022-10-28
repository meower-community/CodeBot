from CodeBot.bot import start_code_bot
import os
import traceback


if __name__ == "__main__":
  try:
    start_code_bot()
    
  except KeyboardInterrupt:
    os.system(f"kill -9 {os.getpid()}")

  traceback.print_exc()
  
  os.system("kill 1")

