from databasemanager import DatabaseManager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime

class FileHandler(FileSystemEventHandler):
    def __init__(self, database, extension=None):

        self.__extension = extension
        self.__filename = None
        self.__filepath = None
        self.database = database

    def on_modified(self, event):
        if event.is_directory: return None
        self.__filename = os.path.basename(event.src_path)
        self.__filepath = os.path.dirname(event.src_path)
        self.log_event('Modified')

    def on_created(self, event):
        if event.is_directory: return None
        self.__filename = os.path.basename(event.src_path)
        self.__filepath = os.path.dirname(event.src_path)
        self.log_event('Created')

    def on_deleted(self, event):
        if event.is_directory: return None
        self.__filename = os.path.basename(event.src_path)
        self.__filepath = os.path.dirname(event.src_path)
        self.log_event('Deleted')

    def log_event(self, event_type):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.database.log_event(self.__filename, self.__filepath, event_type, timestamp)

        #on_any_event: Executed for any event.
        #on_created: Executed upon creation of a new file or directory.
        #on_modified: Executed upon modification of a file or when a directory is renamed.
        #on_deleted: Triggered upon the deletion of a file or directory.
        #on_moved: Triggered when a file or directory is relocated.
class FileWatch:
    def __init__(self, database, extension=None):
        self.__monitoredFiles = []
        self.databaseManager = DatabaseManager(database)
        self.handler = FileHandler(self.databaseManager, extension)
        self.observer = Observer()

    @property
    def monitoredFiles(self):
        return self.__monitoredFiles

    @monitoredFiles.setter
    def monitoredFiles(self, file):
        if os.path.exists(file):
            self.__monitoredFiles.append(file)
            # Optionally, add to observer if required
            self.observer.schedule(self.handler, file, recursive=False)
            print(f"Added and started watching: {file}")
        else:
            print(f"'{file}' is not a valid file or directory.")


    def start(self):
        if not self.__monitoredFiles:
            print('No file to watch')
            return

        for file in self.__monitoredFiles:
            self.observer.schedule(self.handler, file, recursive=False)
            self.observer.start()

        print('Starting file watch... Press Stop to stop')




    def stop(self):
        print('Stopping file watch...')
        self.observer.stop()
        self.databaseManager.close()


#
# watch = FileWatch()
#
#
# # Use the setter to add a new file
# watch.monitoredFiles = "C:/Python/503"
#
# watch.start()

