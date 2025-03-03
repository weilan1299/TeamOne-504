import sqlite3
import time
import tkinter as tk
from tkinter import Menu
import customtkinter
import filewatch
from customtkinter import *
import tkinter.ttk as ttk
from databasemanager import DatabaseManager
from tkinter import StringVar
from observer import Observer
from filewatch import FileWatch
import threading
import queue
import os

# Set appearance mode and default theme
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")


class Tkinter_GUI(Observer):
    def __init__(self, root):

        self.root = root
        self.root.title("File System Watcher")
        self.database = "filewatch.db"

        self.need_update = None
        self.filename = StringVar()
        self.path = StringVar()
        self.event = StringVar()
        self.time = StringVar()

        self.q_filename = StringVar()
        self.q_path = StringVar()
        self.q_event = StringVar()
        self.q_time = StringVar()

        self.entry_var = StringVar()
        self.database_entry = StringVar()

        # Initialize variables
        self.monitor = FileWatch(self.database)
        self.databaseManager = self.monitor.databaseManager
        self.databaseManager.add_observer(self)
        self.root.geometry("800x600")

        # Build the user interface
        self.create_menubar()
        self.create_main_frames()
        self.create_widgets()
        self.table = None

    def create_menubar(self):

        # Creates the application menu bar.
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # File Menu
        file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Start Watching", command=self.start_monitoring)

        file_menu.add_command(label="Stop Watching", command=self.stop_monitoring)
        file_menu.add_command(label="Reset", command=self.reset)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit Menu
        edit_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Browse for directory to watch", command=self.open_directory)

        # Database Menu
        db_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Database", menu=db_menu)
        db_menu.add_command(label="Write", command=self.db_write)
        db_menu.add_command(label="Clear database", command=self.db_clear)
        db_menu.add_command(label="Delete database", command=self.db_delete)
        db_menu.add_command(label="Change database", command=self.db_change)
        db_menu.add_separator()
        db_menu.add_command(label="Query", command=self.query_window)

        # Help Menu
        help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Usage Help", command=self.show_usage)
        help_menu.add_command(label="Shortcut Keys", command=self.show_shortcuts)

    def create_main_frames(self):
        """Creates the main container and subframes."""
        # Main container frame
        self.main_frame = CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Frame 1: Controls (Start, Stop, Reset)
        self.frame1 = CTkFrame(self.main_frame)
        self.frame1.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Frame 2: Directory input and browse
        self.frame2 = CTkFrame(self.main_frame)
        self.frame2.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        # Frame 3: Database settings
        self.frame3 = CTkFrame(self.main_frame)
        self.frame3.grid(row=2, column=0, padx=20, pady=20, sticky="w")

        # Frame 4: Scrollable display for events (log output)
        self.frame4 = CTkScrollableFrame(self.main_frame, orientation="vertical", border_color="#FFCC70",
                                         border_width=3)
        self.frame4.grid(row=3, column=0, padx=20, pady=20, sticky="news")

    def create_widgets(self):
        """Creates and places all widgets in the appropriate frames."""
        # --- Frame 1 Widgets: Control Buttons ---
        self.start_watch_btn = CTkButton(self.frame1, text="Start Watching", corner_radius=20,
                                         cursor="hand2", border_color="#FFCC70", border_width=3,
                                         command=self.start_monitoring)

        self.start_watch_btn.grid(row=0, column=0, padx=5, pady=5)

        self.stop_watch_btn = CTkButton(self.frame1, text="Stop Watching", corner_radius=20,
                                        cursor="hand2", border_color="#FFCC70", border_width=3,
                                        command=self.stop_monitoring)
        self.stop_watch_btn.grid(row=0, column=1, padx=5, pady=5)

        self.reset_btn = CTkButton(self.frame1, text="Reset", corner_radius=20,
                                   cursor="hand2", border_color="#FFCC70", border_width=3, command=self.reset)
        self.reset_btn.grid(row=0, column=2, padx=5, pady=5)

        # --- Frame 2 Widgets: Directory input and Browse ---
        self.path_label = CTkLabel(self.frame2, text="Directory to watch:")
        self.path_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.path_entry = CTkEntry(self.frame2, width=300, placeholder_text="Insert the path to directory",
                                   textvariable=self.entry_var)
        self.path_entry.grid(row=1, column=0, columnspan=8, sticky="w", padx=10, pady=5)

        self.start_btn = CTkButton(self.frame2, text="Start", command=self.start_monitoring)
        self.start_btn.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.stop_btn = CTkButton(self.frame2, text="Stop", command=self.stop_monitoring)
        self.stop_btn.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.browse_btn = CTkButton(self.frame2, text="Browse", command=self.open_directory)
        self.browse_btn.grid(row=2, column=2, padx=10, pady=5)

        self.ext_label = CTkLabel(self.frame2, text="Extension:")
        self.ext_label.grid(row=0, column=9, sticky="w", padx=10, pady=5)

        self.ext_combo = CTkComboBox(self.frame2, values=["", ".txt", ".py", ".exe"])
        self.ext_combo.grid(row=1, column=9, padx=10, pady=5)

        self.watch_checkbox = CTkCheckBox(self.frame2, text="Watch directories?")
        self.watch_checkbox.grid(row=2, column=9, padx=10, pady=5)

        self.info_label = CTkLabel(self.frame2, text="Leave blank for All files")
        self.info_label.grid(row=1, column=10, columnspan=2, sticky="w", padx=10, pady=5)

        # --- Frame 3 Widgets: Database Settings ---
        self.db_label = CTkLabel(self.frame3, text="Database path:")
        self.db_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.db_entry = CTkEntry(self.frame3, width=300, placeholder_text="Database path",
                                 textvariable=self.database_entry)
        self.db_entry.grid(row=1, column=0, columnspan=8, sticky="w", padx=10, pady=5)

        self.write_btn = CTkButton(self.frame3, text="Write", command=self.db_write)
        self.write_btn.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.clear_btn = CTkButton(self.frame3, text="Clear DB", command=self.db_clear)
        self.clear_btn.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.db_browse_btn = CTkButton(self.frame3, text="Browse", command=self.database_path)
        self.db_browse_btn.grid(row=2, column=2, padx=10, pady=5)

        self.db_ext_label = CTkLabel(self.frame3, text="Extension:")
        self.db_ext_label.grid(row=0, column=9, sticky="w", padx=10, pady=5)

        self.db_ext_combo = CTkComboBox(self.frame3, values=["", ".txt", ".py", ".exe"])
        self.db_ext_combo.grid(row=1, column=9, padx=10, pady=5)

        self.event_type_label = CTkLabel(self.frame3, text="Event Type:")
        self.event_type_label.grid(row=0, column=10, sticky="w", padx=10, pady=5)

        self.event_type_combo = CTkComboBox(self.frame3, values=["", "Modified", "Created", "Deleted"])
        self.event_type_combo.grid(row=1, column=10, sticky="w", padx=10, pady=5)

        self.query_btn = CTkButton(self.frame3, text="Query", command=self.db_query)
        self.query_btn.grid(row=2, column=10, padx=10, pady=5)

        # --- Frame 4 Widgets: Scrollable Event Display ---
        self.events_header = CTkLabel(self.frame4, text="File System Watcher Events:")
        self.events_header.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.file_name = CTkLabel(self.frame4, text="File Name")
        self.file_name.grid(row=1, column=0, columnspan=5, sticky="w", padx=5, pady=5)
        self.file_names = CTkLabel(self.frame4, textvariable=self.filename)
        self.file_names.grid(row=2, column=0, columnspan=5, sticky="w", padx=5, pady=5)

        self.path_event = CTkLabel(self.frame4, text="Path")
        self.path_event.grid(row=1, column=6, columnspan=17, sticky="w", padx=5, pady=5)
        self.paths = CTkLabel(self.frame4, textvariable=self.path)
        self.paths.grid(row=2, column=6, columnspan=17, sticky="w", padx=5, pady=5)

        self.event_frame4 = CTkLabel(self.frame4, text="Event Type")
        self.event_frame4.grid(row=1, column=18, columnspan=22, sticky="w", padx=40, pady=5)
        self.event_type = CTkLabel(self.frame4, textvariable=self.event)
        self.event_type.grid(row=2, column=18, columnspan=22, sticky="w", padx=40, pady=5)
        #
        self.time_stamp = CTkLabel(self.frame4, text="Time Stamp")
        self.time_stamp.grid(row=1, column=23, columnspan=25, sticky="e", padx=120, pady=5)
        self.timestamps = CTkLabel(self.frame4, textvariable=self.time)
        self.timestamps.grid(row=2, column=23, columnspan=25, sticky="e", padx=120, pady=5)

    def notify(self, row):

        filename, path, event_type, timestamp = row
        # Append to the StringVars using .set() to update the text
        current_filename = self.filename.get()
        current_path = self.path.get()
        current_event = self.event.get()
        current_time = self.time.get()

        # Concatenate the previous data with new values and update
        self.filename.set(current_filename + filename + "\n")
        self.path.set(current_path + path + "\n")
        self.event.set(current_event + event_type + "\n")
        self.time.set(current_time + timestamp + "\n")  # Add the timestamp with newline

        # Reset the update flag

    # Methods for File System Watching
    def start_monitoring(self):
        """Starts the file system monitoring using watchdog."""

        path = self.entry_var.get()
        if not path:
            print("Please enter a valid path")
            return
        self.monitor.monitoredFiles = path
        self.monitor.start()

    def stop_monitoring(self):
        """Stops the file system monitoring if it is running."""

        self.monitor.stop()

    def reset(self):
        """Resets the directory and database entry fields."""
        pass

    def open_directory(self):
        """Opens a directory selection dialog and sets the selected path."""
        filepath = filedialog.askdirectory()
        if filepath:
            self.entry_var.set(filepath)

    # Methods for Database Operations (Stubs)

    def database_path(self):
        """Opens a directory selection dialog for the database path."""
        file_path = filedialog.askdirectory()
        if file_path:
            self.database_entry.set(file_path)

    def db_write(self):
        print("Database write operation triggered.")
        """write all data downbelow"""
        path = self.db_entry.get()
        file_name = filedialog.asksaveasfilename(
            defaultextension=".db",  # Default extension for database files
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")],  # File types
            title="Save Database As"  # Dialog title
        )
        if not path:
            print("Please enter a valid path")
        self.databaseManager.write_database(path, file_name)


    def db_clear(self):
        print("Database clear operation triggered.")
        self.databaseManager.delete_record()

    def db_delete(self):
        print("Database delete operation triggered.")

    def db_change(self):
        print("Database change operation triggered.")

    def query_window(self):
        print("Database query operation triggered.")
        window = CTk()
        newWindow = tk.Toplevel(window)
        newWindow.title("Database query")
        newWindow.geometry("800x600")
        table_frame = CTkFrame(newWindow)
        table_frame.grid(row=0, column=0, padx=100, pady=20)
        self.table = ttk.Treeview(table_frame, columns = ('File Name', 'Path', 'Event Type', 'Time Stamp'), show="headings", height= 20)
        self.table.grid(row=0, column=0)
        self.table.heading('File Name', text='File Name')
        self.table.heading('Path', text='Path')
        self.table.heading('Event Type', text='Event Type')
        self.table.heading('Time Stamp', text='Time Stamp')
        self.table.column("File Name", width = 200)
        self.table.column("Path", width = 180)
        self.table.column("Event Type", width = 100)
        self.table.column("Time Stamp", width = 120)
        vsb =  ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)


        query_frame = CTkFrame(newWindow)
        query_frame.grid(row=1, column=0, padx=100, pady=20)
        ext_label = CTkLabel(query_frame, text="Extension:")
        ext_label.grid(row=1, column=0, sticky="w", padx=30, pady=5)

        self.q_ext_combo = CTkComboBox(query_frame, values=["", ".txt", ".py", ".exe"])
        self.q_ext_combo.grid(row=2, column=0, sticky="w", padx=20, pady=10)

        event_type = CTkLabel(query_frame, text="Event Type:")
        event_type.grid(row=1, column=1, sticky="w",padx=20, pady=5)

        self.q_event_type_combo = CTkComboBox(query_frame, values=["", "modified", "created", "deleted"])
        self.q_event_type_combo.grid(row=2, column=1, sticky="w",padx=20, pady=10)

        query = CTkButton(query_frame, text="Query", command=self.db_query)
        query.grid(row=2, column=2,sticky="e",padx=30, pady=10)

    def db_query(self):
        extension = self.q_ext_combo.get()
        event_type = self.q_event_type_combo.get()
        data = self.databaseManager.query_data(extension, event_type)




        # Concatenate the previous data with new values and update
        for row in data:
            filename, path, event_type, timestamp = row
            print(filename, path, event_type, timestamp)
            self.table.insert("", "end", values = (filename, path, event_type, timestamp))




    # Methods for Help Menu (Stubs)
    def show_about(self):
        print("Show about information.")

    def show_usage(self):
        print("Show usage help.")

    def show_shortcuts(self):
        print("Show shortcut keys.")


if __name__ == "__main__":
    root = CTk()
    app = Tkinter_GUI(root)
    root.mainloop()