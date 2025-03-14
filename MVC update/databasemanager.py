import sqlite3

import os

import pandas as pd
from nbclient.client import timestamp

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

    def query_data(self, extension, event_type, t1, t2):
        self.connect()

        # file_q = ['extension', 'event_type']
        # for file in file_q:
        #     extension = file
        ext = extension
        et = event_type

        query = """SELECT * FROM filewatch 
                    WHERE filename like ? 
                    And event_type like ? 
                    And STRFTIME('%T', timestamp) > ?
                    And STRFTIME('%T', timestamp) < ?"""

        data = ('%' + ext + '%', '%' + et + '%', t1, t2)
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

