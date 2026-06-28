import sqlite3

DB_PATH = "/home/mike5d/trativod.db"


def get_connection():
    return sqlite3.connect(DB_PATH)
