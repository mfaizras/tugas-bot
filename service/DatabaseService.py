import sqlite3
from sqlite3 import Error
import mysql.connector
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

class MySql:
    def __init__(self):
        load_dotenv()
        self.db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    def cursor(self):
        return self.db.cursor()