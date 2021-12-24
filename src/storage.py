import sqlite3

import config as config

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("res/database.db")
        self.cursor = self.connection.cursor()

        self.create_tables()

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
    
    #private
    def create_tables(self):
        database = config.config.get_baseconfig()["database"]
        for table in database:
            columns = "".join(table["columns"])

            sql_command = f"CREATE TABLE IF NOT EXISTS {table['name']} ({columns});"
            self.cursor.execute(sql_command)

        self.commit()

def init():
    global database
    database = Database()