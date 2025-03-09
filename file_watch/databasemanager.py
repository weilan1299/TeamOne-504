import sqlite3
from observer import Observable
import os


class DatabaseManager(Observable):

    def __init__(self, database = "filewatch.db"):
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

    def query_data(self, extension, event_type):
        self.connect()

        # file_q = ['extension', 'event_type']
        # for file in file_q:
        #     extension = file
        ext = extension
        et = event_type

        query = "SELECT * FROM filewatch WHERE filename like ? And event_type = ?"
        data = ('%ext%', et)
        self.cursor.execute(query, data)

        return self.cursor.fetchall()

    def write_database(self, export_file, file_name):
        self.connect()
        export = os.path.join(export_file, file_name)
        conn = sqlite3.connect(self.database)
        with open(export, 'w') as f:
            for line in conn.iterdump():
                f.write(line)
                f.write('\n')

    def delete_record(self):
        self.connect()
        self.cursor.execute("DELETE FROM filewatch")
        self.conn.commit()

    def drop_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS filewatch")
        self.conn.commit()

    def close(self):
        self.conn.close()


