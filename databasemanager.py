import sqlite3

class DatabaseManager:
    
    def __init__(self):
        self.conn = None

        self.cursor = None

    def create_table(self):
        if self.conn is None:
            self.conn = sqlite3.connect('filewatch.db', check_same_thread=False)
            self.cursor = self.conn.cursor()

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS filewatch (
                                filename TEXT,
                                path TEXT,
                                event_type TEXT,
                                timestamp TEXT )
                                """)

        self.conn.commit()




    def log_event(self, filename, path, event_type, timestamp):
        if self.conn is None:
            self.conn = sqlite3.connect('filewatch.db', check_same_thread=False)
            self.cursor = self.conn.cursor()
        query = "INSERT INTO filewatch (filename, path, event_type, timestamp) VALUES (?, ?, ?, ?)"
        data = (filename, path, event_type, timestamp)
        self.cursor.execute(query, data)

        self.conn.commit()


    def drop_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS filewatch")
        self.conn.commit()


    def close(self):
        self.conn.close()
        self.cursor.close()


