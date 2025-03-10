from databasemanager import DatabaseManager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime
from mvc import Controller

class FileHandler(FileSystemEventHandler):
    def __init__(self, controller,  database, extension=None):

        self.__extension = extension
        self.__filename = None
        self.__filepath = None
        self.controller = controller
        self.database = database

    def on_modified(self, event):
        if event.is_directory: return None
        self.__filename = os.path.basename(event.src_path)  # Extract just the filename
        ext = os.path.splitext(self.__filename)[1]
        self.__filepath = os.path.dirname(event.src_path)
        if ext.lower() in self.__extension:
            self.log_event('Modified')
        elif not self.__extension:
            self.log_event('Modified')

    def on_created(self, event):
        if event.is_directory: return None
        self.__filename = os.path.basename(event.src_path)  # Extract just the filename
        ext = os.path.splitext(self.__filename)[1]
        self.__filepath = os.path.dirname(event.src_path)
        if ext.lower() in self.__extension:
            self.log_event('Created')
        elif not self.__extension:
            self.log_event('Created')

    def on_deleted(self, event):
        if event.is_directory: return None
        self.__filename = os.path.basename(event.src_path)  # Extract just the filename
        ext = os.path.splitext(self.__filename)[1]
        self.__filepath = os.path.dirname(event.src_path)
        if ext.lower() in self.__extension:
            self.log_event('Deleted')
        elif not self.__extension:
            self.log_event('Deleted')

    def log_event(self, event_type):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = self.__filename, self.__filepath, event_type, timestamp
        self.controller.add_row(row)


        #on_any_event: Executed for any event.
        #on_created: Executed upon creation of a new file or directory.
        #on_modified: Executed upon modification of a file or when a directory is renamed.
        #on_deleted: Triggered upon the deletion of a file or directory.
        #on_moved: Triggered when a file or directory is relocated.
class FileWatch(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)
        self.__extension = []
        self.is_running = None
        self.__monitoredFile = []
        self.model = model
        self.view = view
        self.handler = FileHandler(self, model, self.__extension)
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



#
# watch = FileWatch()
#
#
# # Use the setter to add a new file
# watch.monitoredFiles = "C:/Python/503"
#
# watch.start()

