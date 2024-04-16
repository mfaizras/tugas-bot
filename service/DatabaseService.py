import sqlite3
from sqlite3 import Error
from dotenv import load_dotenv
import os

class SqLite:
    def __init__(self):
        load_dotenv()
        dbName = os.getenv('DB_NAME')
        dbName += ".db"

        try:
            self.db = sqlite3.connect(dbName)
        except Error as e:
            print(e)


    def cursor(self):
        return self.db.cursor()