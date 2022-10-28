from os import system
from copy import deepcopy
import json
import uuid

system("replit dump db.json")

# montydb
from montydb import MontyClient, set_storage


set_storage("./db/CodeBot",     
    storage="flatfile",     # storage name, default "flatfile"
    mongo_version="4.0",    # try matching behavior with this mongodb version
    use_bson=True,         # default None, and will import pymongo's bson if None or True

    # any other kwargs are storage engine settings.
    cache_modified=0, 
)

with open("db.json") as f:
  orig_db = json.load(f)
  
new_db =  MontyClient('./db/CodeBot')


orig_db = dict(orig_db)

users = []
for k, usr in orig_db.items():
    if k in ['bans', 'dms']:
        continue
    usr.update({"_id":uuid.uuid4().hex, "username":k})
    users.append(dict(usr))

bans = [{"_id":uuid.uuid4().hex, "username": usr} for usr in orig_db['bans']]
dms = [{"_id":uuid.uuid4().hex,"username": usr, "message": msg} for usr, msg in orig_db['dms'].items()]

new_db.CodeBot.users.insert_many(users)
new_db.CodeBot.bans.insert_many(bans)
new_db.CodeBot.dms.insert_many(dms)