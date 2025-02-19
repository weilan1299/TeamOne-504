import sqlite3
from observer import Observable

class DatabaseManager(Observable):
    
    def __init__(self, database):
        super().__init__()
        self.conn = None
        self.database = database
        self.cursor = None
        self.need_update = False
        self.create_table()

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.database, check_same_thread=False)
            self.cursor = self.conn.cursor()

    def create_table(self):
        self.connect()

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS filewatch (
                                filename TEXT,
                                path TEXT,
                                event_type TEXT,
                                timestamp TEXT )
                                """)

        self.conn.commit()





    def log_event(self, filename, path, event_type, timestamp):
        self.connect()
        if self.conn is None:
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
        query = "INSERT INTO filewatch (filename, path, event_type, timestamp) VALUES (?, ?, ?, ?)"
        data = (filename, path, event_type, timestamp)
        self.cursor.execute(query, data)

        self.conn.commit()


        self.add_row()
        if self.has_added():
            self.notify_observer(self.get_last_event())

    def get_last_event(self):
        self.connect()
        self.cursor.execute("SELECT * FROM filewatch ORDER BY timestamp DESC LIMIT 1")
        return self.cursor.fetchone()


    def drop_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS filewatch")
        self.conn.commit()


    def close(self):
        self.conn.close()
        self.cursor.close()


