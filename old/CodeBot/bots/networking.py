from pathlib import Path

import easy_db
from MeowerBot import Client


class UnderGroundBotNetworking:
    def __init__(self, bot: Client, send_msg):
        self.send_msg = send_msg
        self.bot = bot

        self.ignore_cmds = [
            "__init__",
            "__str__",
            "__repr__",
            "__eq__",
            "__ne__",
            "__hash__",
        ]

        self.db = self._db(self.bot, self)

    class _db:
        def __call__(self, *args, **kwargs):
            if hasattr(self, kwargs["db_cmd"]):
                print(f"Ran SubCommand {kwargs['db_cmd']}")
                return getattr(self, args[0])(**kwargs)
            else:
                self.bot.send_pmsg(
                    {
                        "type": "status",
                        "IsError": True,
                        "error": 404,
                        "msg": "DB Does not have this command",
                    },
                    kwargs.get("raw", {"u": "global"})["origin"],
                )
                return lambda *args, **kwargs: None

        def __init__(self, bot: Client, ubn):
            self.bot = bot
            self.ubn = ubn
            self.dbs = {}

        def create_db(self, **kwargs):
            usr_db = kwargs.get("raw", {"u": "global"})["origin"]
            usr_db = usr_db.replace("/", "").replace(".", "")

            db_path = Path(f"./db/{usr_db}.db")
            try:
                db_path.touch(exist_ok=False)
            except Exception as e:
                self.bot.send_pmsg(
                    {
                        "type": "status",
                        "IsError": True,
                        "error": e.__class__.__name__,
                        "msg": e,
                    },
                    kwargs.get("raw", {"u": "global"})["origin"],
                )
                return

            self.dbs[usr_db] = easy_db.DataBase(db_path)
            self.bot.send_pmsg(
                {"type": "status", "IsError": False, "msg": 200},
                kwargs.get("raw", {"u": "global"})["origin"],
            )

        def create_table(self, **kwargs):
            usr_db = kwargs.get("raw", {"u": "global"})["origin"]
            usr_db = usr_db.replace("/", "").replace(".", "")

            if usr_db not in self.dbs:
                db_path = Path(f"./db/{usr_db}.db")
                if not db_path.exists():
                    self.bot.send_pmsg(
                        {
                            "type": "status",
                            "IsError": True,
                            "error": 404,
                            "msg": "db does not exist",
                        },
                        kwargs.get("raw", {"u": "global"})["u"],
                    )
                    return

                self.dbs[usr_db] = easy_db.DataBase(db_path)

            self.dbs[usr_db].create_table(kwargs["name"], kwargs["columns"])
            self.bot.send_pmsg(
                {"type": "status", "IsError": False, "msg": 200},
                kwargs.get("raw", {"u": "global"})["origin"],
            )
            return

        def insert_row(self, **kwargs):
            usr_db = kwargs.get("raw", {"u": "global"})["u"]
            usr_db = usr_db.replace("/", "").replace(".", "")

            if usr_db not in self.dbs:
                db_path = Path(f"./db/{usr_db}.db")
                if not db_path.exists():
                    self.bot.send_pmsg(
                        {
                            "type": "status",
                            "IsError": True,
                            "error": 404,
                            "msg": "db does not exist",
                        },
                        kwargs.get("raw", {"u": "global"})["u"],
                    )
                    return

                self.dbs[usr_db] = easy_db.DataBase(db_path)

            self.dbs[usr_db].create_table(kwargs["table"], kwargs["columns"])
            self.bot.send_pmsg(
                {"type": "status", "IsError": False, "msg": 200},
                kwargs.get("raw", {"u": "global"})["u"],
            )
            return

        def delete_row(self, **kwargs):
            usr_db = kwargs.get("raw", {"u": "global"})["u"]
            usr_db = usr_db.replace("/", "").replace(".", "")
            if usr_db not in self.dbs:
                db_path = Path(f"./db/{usr_db}.db")
                if not db_path.exists():
                    self.bot.send_pmsg(
                        {
                            "type": "status",
                            "IsError": True,
                            "error": 404,
                            "msg": "db does not exist",
                        },
                        kwargs.get("raw", {"u": "global"})["u"],
                    )
                    return
                self.dbs[usr_db] = easy_db.DataBase(db_path)
            self.dbs[usr_db].drop_column(kwargs["table"], kwargs["column"])
            self.bot.send_pmsg(
                {"type": "status", "IsError": False, "msg": 200},
                kwargs.get("raw", {"u": "global"})["u"],
            )
            return

        def get_row(self, **kwargs):
            usr_db = kwargs.get("raw", {"u": "global"})["u"]
            usr_db = usr_db.replace("/", "").replace(".", "")
            if usr_db not in self.dbs:
                db_path = Path(f"./db/{usr_db}.db")
                if not db_path.exists():
                    self.bot.send_pmsg(
                        {
                            "type": "status",
                            "IsError": True,
                            "error": 404,
                            "msg": "db does not exist",
                        },
                        kwargs.get("raw", {"u": "global"})["u"],
                    )
                    return
                self.dbs[usr_db] = easy_db.DataBase(db_path)
            if "ids" in kwargs and "id_colum" in kwargs:
                self.bot.send_pmsg(
                    {
                        "type": "return",
                        "IsError": False,
                        "status": 200,
                        "data": self.dbs[user_db].pull_where_id_in_list(
                            kwargs["tablename"], kwargs["id_colum"], kwargs["id"]
                        ),
                    },
                    kwargs.get("raw", {"u": "global"})["u"],
                )
            elif "condition" in kwargs:
                self.bot.send_pmsg(
                    {
                        "type": "return",
                        "IsError": False,
                        "status": 200,
                        "data": self.dbs[user_db].pull_where(
                            kwargs["table"], kwargs["condition"]
                        ),
                    },
                    kwargs.get("raw", {"u": "global"})["u"],
                )

            else:
                self.bot.send_pmsg(
                    {
                        "type": "return",
                        "IsError": False,
                        "status": 200,
                        "data": self.dbs[user_db].pull(kwargs["table"]),
                    },
                    kwargs.get("raw", {"u": "global"})["u"],
                )
