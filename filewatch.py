#On program exit, ask the user whether or not to write current contents to the database if those
#contents have not yet been written
#one button should allow the program to start monitoring files, one to stop
#one button should write the current list of monitored files to the database
#a listbox/textbox/combo-box to display information about files that are being watched
#something to allow the user to choose which type of file extension to watch (you should provide a basic
# list of extensions, but also allow the user to specify one)
import sqlite3

import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime

class FileHandler(FileSystemEventHandler):
    def __init__(self, extension = None, ):

        self.extension = extension
        self.filename = None
        self.filepath = None

    def on_modified(self, event):
        if event.is_directory: return None
        self.filename = os.path.basename(event.src_path)
        self.filepath = os.path.dirname(event.src_path)
        self.log_event('modified')

    def on_created(self, event):
        if event.is_directory: return None
        self.filename = os.path.basename(event.src_path)
        self.filepath = os.path.dirname(event.src_path)
        self.log_event('created')

    def on_deleted(self, event):
        if event.is_directory: return None
        self.filename = os.path.basename(event.src_path)
        self.filepath = os.path.dirname(event.src_path)
        self.log_event('deleted')

    def log_event(self, event_type):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('filewatch.db')
        c = conn.cursor()
        query ="INSERT INTO filewatch (filename,path,event_type, timestamp) VALUES (?,?,?,?)"
        data = (self.filename, self.filepath, event_type, timestamp)
        c.execute(query, data)
        conn.commit()
        conn.close()

        #on_any_event: Executed for any event.
        #on_created: Executed upon creation of a new file or directory.
        #on_modified: Executed upon modification of a file or when a directory is renamed.
        #on_deleted: Triggered upon the deletion of a file or directory.
        #on_moved: Triggered when a file or directory is relocated.
class FileWatch:
    def __init__(self, file = None):
        self._monitoredFiles = [file]
        self.database()
        self.handler = FileHandler()
        self.observer = Observer()

    def add_file(self, file):
        self._monitoredFiles.append(file)

    def start(self):
        if not self._monitoredFiles:
            print('No file to watch')
            return

        for file in self._monitoredFiles:
            self.observer.schedule(self.handler, file, recursive=False)
        self.observer.start()

        print('Starting file watch... Press Stop to stop')

        try:
            self.observer.join()
        except KeyboardInterrupt:
            self.exit()


    def database(self):
        conn = sqlite3.connect('filewatch.db')
        c = conn.cursor()
        c.execute("""
                CREATE TABLE IF NOT EXISTS filewatch (
                        filename TEXT,
                        path TEXT,
                        event_type TEXT,
                        timestamp TEXT )
                        """)

        conn.commit()
        conn.close()
    def exit(self):
#ask the user whether or not to write current contents to the database
# if those contents have not yet been written
        pass

watch = FileWatch(r'C:\Python\503')
watch.start()
