import threading
import time

from databasemanager import DatabaseManager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime
import threading

class FileHandler(FileSystemEventHandler):
    def __init__(self, database, extensions):

        self.__extension = extensions
        self.__filename = None
        self.__filepath = None
        self.database = database

    def on_modified(self, event):
        if event.is_directory: return None
        self.__filename, ext = os.path.splitext(event.src_path)
        self.__filepath = os.path.dirname(event.src_path)
        if ext.lower() in self.__extension:
            self.log_event('Modified')
        elif self.__extension==[]:
            self.log_event('Modified')

    def on_created(self, event):
        if event.is_directory: return None
        self.__filename, ext = os.path.splitext(event.src_path)
        self.__filepath = os.path.dirname(event.src_path)
        if ext.lower() in self.__extension:
            self.log_event('Created')
        elif self.__extension==[]:
            self.log_event('Modified')

    def on_deleted(self, event):
        if event.is_directory: return None
        self.__filename, ext = os.path.splitext(event.src_path)
        self.__filepath = os.path.dirname(event.src_path)
        if ext.lower() in self.__extension:
            self.log_event('Deleted')
        elif self.__extension==[]:
            self.log_event('Modified')

    def log_event(self, event_type):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.database.log_event(self.__filename, self.__filepath, event_type, timestamp)

        #on_any_event: Executed for any event.
        #on_created: Executed upon creation of a new file or directory.
        #on_modified: Executed upon modification of a file or when a directory is renamed.
        #on_deleted: Triggered upon the deletion of a file or directory.
        #on_moved: Triggered when a file or directory is relocated.
class FileWatch:
    def __init__(self, database):
        self.is_running = None
        self.__monitoredFile = []
        self.databaseManager = DatabaseManager(database)
        self.__extension = []
        self.handler = FileHandler(self.databaseManager, self.extension)
        self.observer = Observer()

    @property
    def monitoredFile(self):
        return self.__monitoredFile

    @monitoredFile.setter
    def monitoredFile(self, value):
        self.__monitoredFile = value

    @property
    def extension(self):
        return self.__extension
    @extension.setter
    def extension(self, extension):
        self.__extension.append(extension)


    def start(self):
        if not self.__monitoredFile:
            print('No file to watch')
            return
        if self.is_running:
            print("Stopping the current observer...")
            self.stop()

            # Create a new observer instance

        self.observer.schedule(self.handler, self.monitoredFile, recursive=False)
        self.observer.start()

        print("Monitoring started.")

        print('Starting file watch... Press Stop to stop')




    def stop(self):
        print('Stopping file watch...')
        if self.is_running:
            self.observer.stop()
            self.observer.join()  # Wait for the observer to finish its work
            self.is_running = False
            print("Monitoring stopped.")
        else:
            print("Monitoring is not running.")
        self.databaseManager.close()

#
# watch = FileWatch()
#
#
# # Use the setter to add a new file
# watch.monitoredFiles = "C:/Python/503"
#
# watch.start()

