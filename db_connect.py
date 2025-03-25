import sqlite3
from sqlite3 import Connection


def connect_to_db(path: str) -> Connection | None:
    try:
        connection = sqlite3.connect(path)
        return connection
    except sqlite3.Error as e:
        print(f'Could not connect to database: {e}')
        return None
