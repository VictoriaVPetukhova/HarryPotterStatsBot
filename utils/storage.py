import sqlite3


class DatabaseManager(object):
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.insert(
            """
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE
            )
            """
        )

        self.insert(
            """
            CREATE TABLE IF NOT EXISTS spells (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                photo_url TEXT NOT NULL
            )
            """
        )

        self.insert(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                text TEXT NOT NULL
            )
            """
        )

        self.insert(
            """
            CREATE TABLE IF NOT EXISTS spells_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                spell_id INTEGER NOT NULL,
                count INTEGER NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (spell_id) REFERENCES spells(id)
            )
            """
        )

        self.insert(
            """
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT,
                description TEXT NOT NULL,
                photo_url TEXT NOT NULL
            )
            """
        )

        self.insert(
            """
            CREATE TABLE IF NOT EXISTS characters_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                count INTEGER NOT NULL,
                FOREIGN KEY (character_id) REFERENCES characters(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
            """
        )

    def insert(self, arg, values=None):
        if values is None:
            self.cursor.execute(arg)
        else:
            self.cursor.execute(arg, values)
        self.connection.commit()

    def fetchone(self, arg, values=None):
        if values is None:
            self.cursor.execute(arg)
        else:
            self.cursor.execute(arg, values)
        return self.cursor.fetchone()

    def fetchall(self, arg, values=None):
        if values is None:
            self.cursor.execute(arg)
        else:
            self.cursor.execute(arg, values)
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()