import sqlite3
from dataclasses import dataclass


@dataclass()
class Currency:
    code: str
    name: str


class TradeBotDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("tradebot.db")
        self.cursor = self.conn.cursor()
        self.phys_currency_list = []
        self.digi_currency_list = []
        self.startup()

    def startup(self):
        self.create_tables_currs()
        self.get_currencies()

    def create_tables_currs(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS phys_currency_list (
                    currency_code TEXT,
                    currency_name TEXT
                    );""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS digi_currency_list (
                    currency_code TEXT,
                    currency_name TEXT
                    );""")
        self.conn.commit()

    def get_currencies(self):
        phys_rows = self.cursor.execute("""SELECT * FROM phys_currency_list""").fetchall()
        for i in range(len(phys_rows)):
            curr_inst = Currency(code=phys_rows[i][0], name=phys_rows[i][1])
            self.phys_currency_list.append(curr_inst)
        digi_rows = self.cursor.execute("""SELECT * FROM digi_currency_list""").fetchall()
        for i in range(len(digi_rows)):
            curr_inst = Currency(code=digi_rows[i][0], name=digi_rows[1])
            self.digi_currency_list.append(curr_inst)
