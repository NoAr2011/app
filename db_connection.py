import sqlite3


class MainConnection:

    @staticmethod
    def return_main_connection():
        conn = sqlite3.connect("Kalandjatek.db")
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = 0")
        conn.commit()
        return conn