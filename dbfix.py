from json import loads

from replit import db

for k in db.keys():
    try:
        db[k] = loads(db[k])
    except:
        pass

if "bans" not in db:
    db["bans"] = []

if "dms" not in db:
    db["dms"] = {}

#db["ShowierData9978"]['coins'] = 800

