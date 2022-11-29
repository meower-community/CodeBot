"""
  Bot handlers for the @CodeBot system.
"""

import traceback
from replit import db
import copy
from json import loads, dumps


class InternalBot:
  def __init__(self, bot):
      self.bot = bot
      self.bot._wss.callback('on_packet', self._bot_raw_packet)
    
  def send_msg(self, msg, original):
      if original["post_origin"] == "home":
          self.bot.send_msg(msg)
          return
      self.bot._wss.sendPacket(
          {
            "cmd": "direct",
            "val": {
                "cmd": "post_chat",
                "val": {"chatid": original["post_origin"], "p": msg},
            },
          }
      )
  def on_raw_msg(self, msg, lsnr):
      self.handle_msg(msg)


  def on_raw_packet(self, packet, lisn):
      if packet["cmd"] == "direct":
        if "post_origin" in packet["val"].keys():
          self.handle_msg(packet["val"])

  def _bot_raw_packet(self, msg):
    
    packet = loads(msg)
    if packet["cmd"] == "ulist":
      self.on_ulist(packet)
      return
    
    self.bot._bot_packet_handle(dumps(packet))

  def on_ulist(self, *args, **kwargs):
        if not self.bot.authed:
          return
        users = self.bot._wss.statedata['ulist']['usernames']

        for user in users:
          dm = self.bot.db.CodeBot.dms.find_one({'username': user})
          if dm:
            self.bot.send_msg(dm["message"])
            self.bot.db.CodeBot.dms.delete_one({"username": user})
            return

  def handle_pmsg(self, msg, origin, _):
      if not type(msg['val']) is dict:
        return
        
      if hasattr(self.bot.ubl, msg['val']['cmd']):
        try:
          
            getattr(self.bot.ubl, msg['val']['cmd'])(**msg['val'], raw=msg)
            print(f"Ran Command '{msg['val']['cmd']}'")
        except Exception as e:

            self.send_msg(f"Uh Oh:\n Exception: {e.__class__.__name__}:", msg)
            print(traceback.print_exc())
      

  def handle_msg(self, msg):
    try:
      print(f"chat: {msg['post_origin']}\n{msg['u']}: {msg['p']}")
      if msg["u"] == "Discord":
          msg["u"] = msg["p"].split(":")[0]
          msg["p"] = msg["p"].split(":")[1].strip()

  
      args = msg["p"].split(" ")
  
      if not self.bot.handle.handle_pre_msg(args, msg, self.bot):
        return
    
      if hasattr(self.bot.cmds, args[1]):
              getattr(self.bot.cmds, args[1])(*args[2:], raw=msg)
              print(f"Ran Command '{args[1]}'")
  
      else:
          self.send_msg(f"@{msg['u']} '{args[1]}' is not one of my commands", msg)
    except (KeyError, IndexError) as e:
      self.send_msg(f"Uh Uh You missed a arg for the cmd {args[1]}", msg)
  
    except Exception as e:
            self.send_msg(f"Uh Oh:\n Exception: {e.__class__.__name__}:", msg)
            print(traceback.print_exc())
