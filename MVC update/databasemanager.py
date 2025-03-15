import sqlite3

import os

import pandas as pd


from mvc import Model


class DatabaseManager(Model):

    def __init__(self, database="filewatch.db"):


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

    def add_row(self, row):

        self.connect()
        if self.conn is None:
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
        query = "INSERT INTO filewatch (filename, path, event_type, timestamp) VALUES (?, ?, ?, ?)"
        filename, path, event_type, timestamp = row

        self.cursor.execute(query, (filename, path, event_type, timestamp))

        self.conn.commit()
        self.rows.append(row)

    def get_all(self):
        self.connect()
        self.cursor.execute("SELECT * FROM filewatch ORDER BY timestamp DESC")
        return self.cursor.fetchall()

    def query_data(self, extension, event_type, date, t1, t2):
        self.connect()
        query = "SELECT * FROM filewatch WHERE 1=1"
        arg = []

        # Add filters based on the parameters
        if extension:  # If an extension is provided, filter by filename
            query += " AND filename LIKE ?"
            arg.append('%' + extension + '%')

        if event_type:  # If an event type is provided, filter by event_type
            query += " AND event_type LIKE ?"
            arg.append('%' + event_type + '%')

        if date:  # If a date is provided, filter by date
            query += " AND STRFTIME('%F', timestamp) = ?"
            arg.append(date)

        if t1 and t2:  # If both time range values are provided, filter by time
            query += " AND STRFTIME('%T', timestamp) > ? AND STRFTIME('%T', timestamp) < ?"
            arg.append(t1)
            arg.append(t2)

        self.cursor.execute(query, tuple(arg))

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

    def export_db_to_csv(self):
        self.connect()

        self.sqlquery = "SELECT * FROM filewatch"


        df = pd.read_sql_query(self.sqlquery, self.conn)
        self.filename = 'filewatch.csv'
        df.to_csv(self.filename, index=False)
        return self.filename

    def close(self):
        self.conn.close()
        self.cursor.close()
