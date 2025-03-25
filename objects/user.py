import sqlite3
from sqlite3 import Connection


class User:
    id = 0

    def __init__(self, url='', email='', first_name='', last_name=''):
        self.url = url
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def save(self, db_connection: Connection) -> bool:
        flag = False
        cursor = None
        try:
            cursor = db_connection.cursor()
            cursor.execute("""
                INSERT INTO users (url, email, first_name, last_name) VALUES (?,?,?,?)
            """, (self.url, self.email, self.first_name, self.last_name))
            db_connection.commit()
            flag = True
        except sqlite3.Error as e:
            print(f'Error occurred while inserting user data: {e}')
        finally:
            if cursor: cursor.close()
            return flag

    @staticmethod
    def create_table(db_connection: Connection) -> bool:
        flag = False
        cursor = None
        try:
            cursor = db_connection.cursor()
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            url TEXT,
                            email TEXT, 
                            first_name TEXT NOT NULL, 
                            last_name TEXT
                        )
                    """)
            db_connection.commit()
            flag = True
        except sqlite3.Error as e:
            print(f'Error occurred while creating users table: {e}')
        finally:
            if cursor: cursor.close()
            return flag

    def delete_user(self, db_connection: Connection) -> bool:
        flag = False
        cursor = None
        try:
            cursor = db_connection.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (self.id,))
            db_connection.commit()
            if cursor.rowcount <= 0:
                print(f'User with id {self.id} did not exist')
            flag = True
        except sqlite3.Error as e:
            print(f'Error occurred while creating user table: {e}')
        finally:
            if cursor: cursor.close()
            return flag

    def __str__(self):
        return f'id:{self.id} first_name:{self.first_name} last_name:{self.last_name} email:{self.email} url:{self.url}'


def get_user_by_email(db_connection: Connection, email: str) -> None | User:
    user = None
    cursor = None
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email like '%?%'", (email,))
        row = cursor.fetchone()
        user = User(row[1], row[2], row[3], row[4])
        user.id = row[0]
    except sqlite3.Error as e:
        print(f'Error occurred while creating user table: {e}')
    finally:
        if cursor: cursor.close()
    return user


def get_all_users(db_connection: Connection) -> [User]:
    users = []
    cursor = None
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user = User(row[1], row[2], row[3], row[4])
            user.id = row[0]
            users.append(user)
    except sqlite3.Error as e:
        print(f'Error occurred while creating user table: {e}')
    finally:
        if cursor: cursor.close()
    return users
