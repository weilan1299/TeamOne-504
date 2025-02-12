#On program exit, ask the user whether or not to write current contents to the database if those
#contents have not yet been written
#one button should allow the program to start monitoring files, one to stop
#one button should write the current list of monitored files to the database
#a listbox/textbox/combo-box to display information about files that are being watched
#something to allow the user to choose which type of file extension to watch (you should provide a basic
# list of extensions, but also allow the user to specify one)
import time
import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self, textbox, extension = None, ):
        self.textbox = textbox
        self.extension = extension

    def on_modified(self, event):
        if event.is_directory: return None
        self.textbox.insert(tk.END, f'File {event.src_path} has been modified')

    def on_created(self, event):
        if event.is_directory: return None
        self.textbox.insert(tk.END, f'File {event.src_path} has been created')

    def on_deleted(self, event):
        if event.is_directory: return None
        self.textbox.insert(tk.END, f'File {event.src_path} has been deleted')


        #on_any_event: Executed for any event.
        #on_created: Executed upon creation of a new file or directory.
        #on_modified: Executed upon modification of a file or when a directory is renamed.
        #on_deleted: Triggered upon the deletion of a file or directory.
        #on_moved: Triggered when a file or directory is relocated.
class FileWatch:
    def __init__(self, text, file = None):
        self._monitoredFiles = [file]
        self.__text = text
        self.handler = FileHandler(text)
        self.observer = Observer()

    def add_file(self, file):
        self.monitoredFiles.append(file)

    def start(self):
        if not self.monitoredFiles:
            self.text.insert(tk.END, 'No file to watch')
            return

        for file in self.monitoredFiles:
            self.observer.schedule(self.handler, file, recursive=False)
        self.observer.start()
        self.text.insert(tk.END, 'Starting file watch... Press Stop to stop')

    def save_to_database(self):
        pass
    def exit(self):
#ask the user whether or not to write current contents to the database
# if those contents have not yet been written
        pass

