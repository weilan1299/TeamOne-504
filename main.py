import csv
import os

import smtplib
import threading
import tkinter as tk
from email.message import EmailMessage


from tkinter import Menu, messagebox
import customtkinter
from customtkinter import *
import tkinter.ttk as ttk

from dotenv import load_dotenv

from databasemanager import DatabaseManager
from tkinter import StringVar
from mvc import View
from filewatch import FileWatch



# Set appearance mode and default theme
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")
load_dotenv()

class Tkinter_GUI(View):
    def __init__(self, root):
        self.__root = root
        self.__root.title("File System Watcher")
        self.database = "filewatch.db"


        self.__filename = StringVar()
        self.__path = StringVar()
        self.event = StringVar()
        self.time = StringVar()

        self.check_var = IntVar()

        self.entry_var = StringVar()
        self.database_entry = StringVar()
        self.q_data = None

        # Initialize variables
        self.model = None
        self.controller = None


        self.__root.geometry("850x700")

        # Build the user interface
        self.create_menubar()
        self.create_main_frames()
        self.create_widgets()
        self.table = None
        self.__saved = False


        root.protocol("WM_DELETE_WINDOW", self.exit)
    def create_menubar(self):

        """Creates the application menu bar."""

        self.menubar = Menu(self.__root)
        self.__root.config(menu=self.menubar)

        # File Menu
        file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Start Watching", command=self.start_monitoring)

        file_menu.add_command(label="Stop Watching", command=self.stop_monitoring)
        file_menu.add_command(label="Reset", command=self.reset)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.__root.quit)

        # Edit Menu
        edit_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Browse for directory to watch", command=self.open_directory)

        # Database Menu
        db_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Database", menu=db_menu)
        db_menu.add_command(label="Write", command=self.db_write)
        db_menu.add_command(label="Clear database", command=self.db_clear)

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
        self.main_frame = CTkFrame(self.__root)
        self.main_frame.pack(fill="both", expand=True)


        # Frame 1: Controls (Start, Stop, Reset)
        self.frame1 = CTkFrame(self.main_frame)
        self.frame1.grid(row=0, column=0,padx=20, pady=20, sticky="w")


        # Frame 2: Directory input and browse
        self.frame2 = CTkFrame(self.main_frame)
        self.frame2.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        # Frame 3: Database settings
        self.frame3 = CTkFrame(self.main_frame)
        self.frame3.grid(row=2, column=0,padx=20, pady=20, sticky="w")

        # Frame 4: Scrollable display for events (log output)
        self.frame4 = CTkFrame(self.main_frame)
        self.frame4.grid(row=3, column=0, padx=20, pady=20, sticky="news")

        self.scrollbar = CTkScrollbar(self.frame4)
        self.scrollbar.pack(side="right", fill="y")

    def create_widgets(self):
        """Creates and places all widgets in the appropriate frames."""
        # --- Frame 1 Widgets: Control Buttons ---
        self.start_watch_btn = CTkButton(self.frame1, text="Start Watching", corner_radius=20,
                                         cursor="hand2", border_color="#FFCC70", border_width=3,
                                         command=self.start_monitoring)

        self.start_watch_btn.grid(row=0, column=0, padx=5, pady=5)
        self.__root.bind("<Control-s>", lambda event: self.start_monitoring())


        self.stop_watch_btn = CTkButton(self.frame1, text="Stop Watching", corner_radius=20,
                                        cursor="hand2", border_color="#FFCC70", border_width=3,
                                        command=self.stop_monitoring)
        self.stop_watch_btn.grid(row=0, column=1, padx=5, pady=5)
        self.__root.bind("<Control-q>", lambda event: self.stop_monitoring())

        self.reset_btn = CTkButton(self.frame1, text="Reset", corner_radius=20,
                                   cursor="hand2", border_color="#FFCC70", border_width=3, command=self.reset)
        self.reset_btn.grid(row=0, column=2, padx=5, pady=5)
        self.__root.bind("<Control-r>", lambda event: self.reset())

        # --- Frame 2 Widgets: Directory input and Browse ---
        path_label = CTkLabel(self.frame2, text="Directory to watch:")
        path_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        path_entry = CTkEntry(self.frame2, width=300, placeholder_text="Insert the path to directory",
                                   textvariable=self.entry_var)
        path_entry.grid(row=1, column=0, columnspan=8, sticky="w", padx=10, pady=5)

        start_btn = CTkButton(self.frame2, text="Start", command=self.start_monitoring)
        start_btn.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        stop_btn = CTkButton(self.frame2, text="Stop", command=self.stop_monitoring)
        stop_btn.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        browse_btn = CTkButton(self.frame2, text="Browse", command=self.open_directory)
        browse_btn.grid(row=2, column=2, padx=10, pady=5)
        self.__root.bind("<Control-b>", lambda event: self.open_directory())

        ext_label = CTkLabel(self.frame2, text="Extension:")
        ext_label.grid(row=0, column=9, sticky="w", padx=10, pady=5)

        self.ext_combo = CTkComboBox(self.frame2, values=["", ".txt", ".py", ".exe"])
        self.ext_combo.grid(row=1, column=9, padx=10, pady=5)

        self.watch_checkbox = CTkCheckBox(self.frame2, text="Watch directories?", variable=self.check_var,
                                                      command=self.check)
        self.watch_checkbox.grid(row=2, column=9, padx=10, pady=5)

        info_label = CTkLabel(self.frame2, text="Leave blank for All files")
        info_label.grid(row=1, column=10, columnspan=2, sticky="w", padx=10, pady=5)

        # --- Frame 3 Widgets: Database Settings ---
        db_label = CTkLabel(self.frame3, text="Database path:")
        db_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.db_entry = CTkEntry(self.frame3, width=300, placeholder_text="Database path",
                                 textvariable=self.database_entry)
        self.db_entry.grid(row=1, column=0, columnspan=8, sticky="w", padx=10, pady=5)

        write_btn = CTkButton(self.frame3, text="Write", command=self.db_write)
        write_btn.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        clear_btn = CTkButton(self.frame3, text="Clear DB", command=self.db_clear)
        clear_btn.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        db_browse_btn = CTkButton(self.frame3, text="Browse", command=self.database_path)
        db_browse_btn.grid(row=2, column=2, padx=10, pady=5)

        db_m = CTkLabel(self.frame3, text="Database manage:")
        db_m.grid(row=0, column=10, sticky="w", padx=40, pady=5)
        query_btn = CTkButton(self.frame3, text="Query Database", command=self.query_window)
        query_btn.grid(row=2, column=10, padx=40, pady=5)

        #Email Button to send the database file
        email = CTkButton(self.frame3, text = "Email Database", command=self.email_data)
        email.grid(row=1, column=10, padx=40, pady=5)
        self.__root.bind("<Control-e>", lambda event: self.email_data())


        # --- Frame 4 Widgets: Logging event for database ---
        self.treeview = ttk.Treeview(self.frame4, yscrollcommand=self.scrollbar.set, selectmode="extended")
        self.treeview.pack(fill="both", expand=True)
        self.scrollbar.configure(command=self.treeview.yview)

        #Create 4 columns for logging event
        self.treeview['columns'] = ("File Name", "Path", "Event Type", "Time Stamp")
        self.treeview.column('#0', width=0, stretch=NO)
        self.treeview.column("File Name", anchor=W, width=120)
        self.treeview.column("Path", anchor=CENTER, width=200)
        self.treeview.column("Event Type", anchor=W, width=120)
        self.treeview.column("Time Stamp", anchor=CENTER, width=120)

        # creating the heading
        self.treeview.heading("File Name", text="File Name", anchor=W)
        self.treeview.heading("Path", text="Path", anchor=CENTER)
        self.treeview.heading("Event Type", text="Event Type", anchor=W)
        self.treeview.heading("Time Stamp", text="Time Stamp", anchor=CENTER)

    def check(self):
        """Check if the checkbox is checked"""
        return self.check_var.get()

    def show_data(self, rows):
        """Displays the data in the treeview."""

        # Initialize empty strings to store accumulated data
        filename_data = ""
        path_data = ""
        event_data = ""
        time_data = ""

        # Loop through each row and append the values to the respective string variables
        for row in rows:
            self.row = row
            filename, path, event_type, timestamp = self.row

            # Append each row's data to the accumulated string for each field
            filename_data += filename + "\n"
            path_data += path + "\n"
            event_data += event_type + "\n"
            time_data += timestamp + "\n"

        # After the loop, set all the StringVars with the concatenated data
        self.__filename.set(filename_data)
        self.__path.set(path_data)
        self.event.set(event_data)
        self.time.set(time_data)

        # Adding some style
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', background='white')

        # Adding rows to the treeview
        self.treeview.insert("", "end", values=self.row)
        # Reset the update flag
        self.__saved = False

    # Methods for File System Watching
    def start_monitoring(self):
        """Starts the file system monitoring using watchdog."""

        path = self.entry_var.get()
        if not path:
            messagebox.showinfo("Error", "Please enter a valid path")
            return
        self.controller.monitoredFile = path
        if self.ext_combo.get() != "":
            ext = self.ext_combo.get()
            print(ext)
            self.controller.extension = ext
            print(self.controller.extension)
        self.controller.start()
        self.start_watch_btn.configure(text="Monitoring...", state=tk.DISABLED)
        if hasattr(self, "start_btn"):
            self.start_btn.configure(state=tk.DISABLED)

        # watch directory check or not, to decided to watch subdirectory

    def stop_monitoring(self):
        """Stops the file system monitoring if it is running."""

        path = self.entry_var.get()

        if not path:
            messagebox.showinfo("Error", "Please enter a valid path")
            return
        if messagebox.askyesno("Stop Monitoring", "Are you sure you want to Stop Monitoring?"):
            self.controller.stop()
            self.start_watch_btn.configure(text="Start Monitoring", state=tk.NORMAL)
            if hasattr(self, "start_btn"):
                self.start_btn.configure(state=tk.NORMAL)
        else:
            self.start_watch_btn.configure(text="Monitoring...", state=tk.DISABLED)

    def reset(self):
        """Resets the directory and database entry fields."""

        #empty database, empty all entries
        self.__filename.set("")
        self.__path.set("")
        self.event.set("")
        self.time.set("")
        self.entry_var.set("")
        self.database_entry.set("")
        self.treeview.delete(*self.treeview.get_children())

    def open_directory(self):
        """Opens a directory selection dialog and sets the selected path."""
        filepath = filedialog.askdirectory()
        if filepath:
            self.entry_var.set(filepath)



    def database_path(self):
        """Opens a directory selection dialog for the database path."""
        file_path = filedialog.askdirectory()
        if file_path:
            self.database_entry.set(file_path)

    def db_write(self):
        """Writes the database to a file as db or csv extension."""

        path = self.db_entry.get()
        file_name = filedialog.asksaveasfilename(
            defaultextension=".csv",  # Default extension for database files
            filetypes=[("Database", "*.db"),("MS Excel", '*.csv'), ("All Files", "*.*")],  # File types
            title="Save Database As"  # Dialog title
        )
        try:
            if not path:
                self.model.write_database(path, file_name)
                self.__saved = True
                messagebox.showinfo("Success", "File successfully saved")
        except Exception as e:
            messagebox.showinfo("Error", "Error writing to database.")
            print("Error writing to database:", e)


    def db_clear(self):
        """Clears the database of all records."""
        try:

            ask_user = messagebox.askyesno("Clear Database", "Are you sure you want to clear the database?")
            if ask_user:
                print("Database clear operation triggered.")
                self.model.delete_record()
                self.__filename.set("")
                self.__path.set("")
                self.event.set("")
                self.time.set("")

                messagebox.showinfo('Success', 'Database cleared')
        except Exception as e:
            print(e)

    def download_usage(self):
        """Downloads the usage message to a text file."""
        file = filedialog.asksaveasfile(defaultextension='.txt', filetypes=[("Text Files", "*.txt"),
                                                                            ("Python Files", "*.py"),
                                                                            ("All Files", "*.*")])
        if file:
            try:
                file_text = str(self.usage_message)
                file.write(file_text)
                file.close()
                print(f"Usage message has been saved to {file}")
            except Exception as e:
                print("Error saving usage:", e)

    def email_data(self):
        """Creates email frame"""
        self.email_window = CTkFrame(self.__root)
        self.new_window = tk.Toplevel(self.email_window)
        self.new_window.title("Send Email")
        self.new_window.geometry("400x300")
        self.email_entry = CTkEntry(self.new_window, width=200, placeholder_text='Please enter your email address')
        self.send_button = CTkButton(self.new_window, text="Send", command=self.send_email_in_thread)
        self.exit_button = CTkButton(self.new_window, text="Exit", command=self.new_window.destroy)
        self.progress_bar = CTkProgressBar(self.new_window, mode="indeterminate")

        self.progress_bar.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.progress_bar.set(0)

        self.email_window.pack(fill=tk.BOTH, expand=True)
        self.email_entry.grid(row=0, column=0, padx=5, pady=50, columnspan=4, sticky="news")
        self.send_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.exit_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # To make the root window disabled while the new_window is still open
        self.new_window.transient(self.__root)
        self.new_window.grab_set()
        self.email_window.wait_window()




    def send_email_in_thread(self):

        """Sends the email in a separate thread."""

        self.progress_bar.set(0)
        self.progress_bar.start()
        self.send_button.configure(state='disabled')

        email_thread = threading.Thread(target=self.send_email)
        email_thread.start()
        self.check_thread_status(email_thread)

    def check_thread_status(self, thread):
        """Checks the status of the email thread."""
        if thread.is_alive():
            self.__root.after(100, lambda: self.check_thread_status(thread))
        else:
            self.progress_bar.stop()
            self.progress_bar.set(0)
            self.send_button.configure(state='normal')

    def send_email(self):
        """Sends the email with the database file as a csv attachment."""

        try:
                EMAIL_ADDRESS = os.getenv('FILE_EMAIL')
                EMAIL_PASS = os.getenv('FILE_PASSWORD')
                email = self.email_entry.get()
                msg = EmailMessage()
                msg["Subject"] = "Events from Filewatcher..."
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = email
                msg.set_content("Events from database...")

                csv_file = self.model.export_db_to_csv()
                with open(csv_file, "rb") as f:
                    file_data = f.read()
                    file_name = f.name
                msg.add_attachment(file_data, maintype="application", subtype="octet", filename=file_name)

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
                    smtp.send_message(msg)

                self.__root.after(0, lambda: messagebox.showinfo("Success", "Email has been sent."))

        except Exception as e:
                self.__root.after(0, lambda: messagebox.showinfo("Error", "Could not send email."))

                print("Error sending email:", e)

        finally:
                self.__root.after(0, lambda: self.send_button.configure(state='normal'))



    def query_window(self):
        """Creates the query window."""
        self.window = CTkFrame(self.__root)
        self.newWindow = tk.Toplevel(self.window)
        self.newWindow.title("Database query")
        self.newWindow.geometry("800x700")
        table_frame = CTkFrame(self.newWindow)
        table_frame.grid(row=0, column=0, padx=100, pady=20)
        self.table = ttk.Treeview(table_frame, columns=('File Name', 'Path', 'Event Type', 'Time Stamp'),
                                  show="headings", height=20)
        self.table.grid(row=0, column=0)
        self.table.heading('File Name', text='File Name')
        self.table.heading('Path', text='Path')
        self.table.heading('Event Type', text='Event Type')
        self.table.heading('Time Stamp', text='Time Stamp')
        self.table.column("File Name", width=200)
        self.table.column("Path", width=180)
        self.table.column("Event Type", width=100)
        self.table.column("Time Stamp", width=140)
        ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)


        query_frame = CTkFrame(self.newWindow)
        query_frame.grid(row=1, column=0, padx=100, pady=20)
        ext_label = CTkLabel(query_frame, text="Extension:")
        ext_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.q_ext_combo = CTkComboBox(query_frame, values=["", ".txt", ".py", ".exe"])
        self.q_ext_combo.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        event_type = CTkLabel(query_frame, text="Event Type:")
        event_type.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.q_event_type_combo = CTkComboBox(query_frame, values=["", "modified", "created", "deleted"])
        self.q_event_type_combo.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        date = CTkLabel(query_frame, text="Date: YYYY-MM-DD")
        date.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.date = CTkEntry(query_frame, placeholder_text="YYYY-MM-DD")
        self.date.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        time_range = CTkLabel(query_frame, text="Time Range: hh:mm:ss; hh:0-24, mm:0-60, ss:0-60")
        time_range.grid(row=3, column=1, columnspan = 2,sticky="w", padx=15, pady=0)

        self.time_entry1 = CTkEntry(query_frame, placeholder_text="00:00:00")
        self.time_entry1.grid(row=4, column=1, sticky="w", padx=10, pady=10)

        self.time_entry2 = CTkEntry(query_frame, placeholder_text="00:00:00")
        self.time_entry2.grid(row=4, column=2, sticky="w", padx=10, pady=10)

        email = CTkButton(query_frame, text="Email", command=self.q_email_data)
        email.grid(row=1, column=2, sticky="e", padx=30, pady=10)


        query = CTkButton(query_frame, text="Query", command=self.db_query)
        query.grid(row=2, column=2, sticky="e", padx=30, pady=10)

        # To make the root window disabled while the new_window is still open
        self.newWindow.transient(self.__root)
        self.newWindow.grab_set()
        self.window.wait_window()

    def db_query_thread(self):
        """Executes the database query in a separate thread"""
        self.q_progress_bar.set(0)
        self.q_progress_bar.start()
        self.q_send_button.configure(state='disabled')

        q_email_thread = threading.Thread(target=self.q_send_email)
        q_email_thread.start()
        self.check_query_thread_status(q_email_thread)

    def check_query_thread_status(self, thread):
        """Checks the status of the query thread."""

        if thread.is_alive():
            self.__root.after(100, lambda: self.check_query_thread_status(thread))
        else:
            self.q_progress_bar.stop()
            self.q_progress_bar.set(0)
            self.q_send_button.configure(state='normal')

    def q_email_data(self):
        """Creates the email frame for the query data."""
        q_email_window = CTkFrame(self.__root)
        new_q_window = tk.Toplevel(q_email_window)
        new_q_window.title("Send Email")
        new_q_window.geometry("400x300")
        self.q_email_entry = CTkEntry(new_q_window, width=200, placeholder_text='Please enter your email address')
        self.q_send_button = CTkButton(new_q_window, text="Send", command=self.db_query_thread)
        exit_button = CTkButton(new_q_window, text="Exit", command=new_q_window.destroy)

        self.q_progress_bar = CTkProgressBar(new_q_window, mode="indeterminate")
        self.q_progress_bar.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.q_progress_bar.set(0)

        q_email_window.pack(fill=tk.BOTH, expand=True)
        self.q_email_entry.grid(row=0, column=0, padx=5, pady=50, columnspan=4, sticky="news")
        self.q_send_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        exit_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # To make the root window disabled while the new_window is still open
        new_q_window.transient(self.__root)
        new_q_window.grab_set()
        q_email_window.wait_window()

    def q_send_email(self):
        """Sends the email with the query data as a csv attachment."""

        try:
            EMAIL_ADDRESS = os.getenv("FILE_EMAIL")
            EMAIL_PASS = os.getenv('FILE_PASSWORD')
            email = self.q_email_entry.get()
            msg = EmailMessage()
            msg["Subject"] = "Filtered data from database..."
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = email
            msg.set_content("Query data...")


            with open("query.csv", "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["filename", "path", "event_type", "timestamp"])
                writer.writerows(self.q_data)

            file_name = "query.csv"
            with open(file_name, "rb") as file:
                file_data = file.read()

            # Add the attachment to the email
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)


            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
                    smtp.send_message(msg)
                    # messagebox.showinfo("Send Email", "Email has been sent.")

            self.__root.after(0, lambda: messagebox.showinfo("Success", "Query Email has been sent."))

        except Exception as e:
                self.__root.after(0, lambda: messagebox.showinfo("Error", "Could not send email."))

                print("Error sending email:", e)

        finally:
            self.__root.after(0, lambda: self.q_send_button.configure(state='normal'))

    def db_query(self):
        """Queries the database based on the user's input like extension, event type, and date."""
        for item in self.table.get_children():
            self.table.delete(item)
        extension = self.q_ext_combo.get()
        event_type = self.q_event_type_combo.get()
        date = self.date.get()

        t1 = self.time_entry1.get()
        t2 = self.time_entry2.get()

        try:
            self.q_data = self.model.query_data(extension, event_type, date, t1, t2)

            # Check if any data was returned
            if not self.q_data:
                messagebox.showinfo('No Results', "No data found matching the given criteria.")
        except Exception as e:
            # Handle any errors in the query execution
            messagebox.showinfo('Error', f"Could not query the database. Error: {str(e)}")
            print(f"Error executing query: {e}")

        for row in self.q_data:
            filename, path, event_type, timestamp = row
            self.table.insert("", "end", values=(filename, path, event_type, timestamp))


    def show_usage(self):
        """Show the usage of the application to the user"""
        self.new = CTkToplevel()
        self.new.title("Usage")
        self.usage_message = """
        
        Usage Guide: To use this File System Watcher application, your desktop computer, 
                laptop, or other device should operates latest versions of windows, mac, or Linux
                etc. The File System Watcher application, was built using python 3.12, thus your device should be 
                able to operate this python version.
                
        A) Top Left Corner: The window has four small buttons, named as "File", "Edit", 
            "Database", and "Help".
            1. File: Clicking this button, will allow user/you to see small dropdown button, consisting 
                "Start Watching", "Stop Watching", "Rest", and "Exit"
            2. Edit: Clicking this button will allow user/you to browse and select a directory, 
                or target file that you want or plan to be watched accordingly.
            3. Database: Clicking this button will allow user/you to see small dropdown button,
                consisting "Write","Clear database", and "Query".
            4. Help: Clicking this button will allow the user/you to access small dropdown 
                button, consisting of the "About", "Usage Help", and "Shortcut Keys".
        B) Where to watch: First a user/you should determine which directory, or
            file to watch do your selection of targets accordingly:
            
            1. To start watching a directory/ies, enter the directory path either clicking the "Edit"
                button at the top left corner or the "Browse" button under the directory to watch,
                then proceed browsing and selecting your target directory, or file. Specify your
                target using the "Extension" button by choosing either a file to be ".txt", ".py",
                or ".exe". Or leave the "Extension" button blank if you prefer to watch and monitor
                all directories and click the "Watch directories" box found on the right of "Browse"
                button and bellow the "Extension" dropdown button.
                
            2. Then click "Start Watching" or "Start" buttons on the display or by dropping down
                the "File" button on the top-left corner, from this click the "Start Watching" button.
                
            3. You can stop monitoring by clicking "Stop Watching" or "Stop" button, Or click "File"
                button on the top-left corner, then from this click "Stop Watching" button.
            4. Reset: To change the directory the user/you want to watch, 
                click the "Reset" button. This will allow the user to clear any directory/ies 
                he/she/it selected and choose another directory.
                
        C) Database Management: The user have the following options for data management.
            1. Click the "Browse" button under the Database path, then select where to store
                the output/result of the files or directory/ies the File Watcher System watched.
                
            2. Write: Click the "Write" button either bellow the Database path or from the "Database" 
                on the top-left corner. This will allow the user to write the data to a specified
                file or directory/ies.
                
            3. Clear DB/Clear database: Click the "Clear DB" or "Clear database" buttons to clear the output/result of 
                the watched files before the result is stored to an specified file or directory/ies. or click 
                Database button, then a dropdown will pop-up then, click Clear database, this will also clear the 
                data watched.
                
                
            4. Click the "Change database" under the "Database" button to modify stored 
                output/result data.
                
            5. Query: Click the "Query" button under the "Database" button or the "Query" button to 
                query stored output/result of any database. A user can specify the type of 
                query by selecting the drop-down options under the Extension indicator and
                drop-down options under the Event Type and above the "Query" button.
                
            6. File Watcher System Events will appear the last box of the window and will 
                have a File Name, Path, Event Type, and Time Stamp in real-time occurrence.
                
            7. Email Database: To send the data watched in to you email, click Email Database
                then follow the instructions provided like inserting properly your email.
            8. Query Email: Send the query data as a csv file. 
        """
        use = CTkLabel(self.new, text=self.usage_message)
        use.pack()
        save = CTkButton(self.new, text="Download", command=self.download_usage)
        save.pack()

    def show_shortcuts(self):
        # Shortcut keys message popup
        short = CTkToplevel()
        short.title("Shortcuts")
        shortcuts_message = """
                   Keyboard Shortcuts:

                   - Ctrl + S: Start Watching
                   - Ctrl + Q: Stop Watching
                   - Ctrl + R: Reset
                   - Ctrl + B: Browse Directory
                   - Ctrl + E: Email Database
                   These shortcuts help you navigate and use the app quickly.
                   """
        keys = CTkLabel(short, text=shortcuts_message)
        keys.pack()
    def show_about(self):

        top = CTkToplevel()
        top.title("About")
        about_message = """This File System Watcher application is version 1.0.
                   Authors: Weilan Liang
                            Dereje Teshager
                            Aden Abdulahi
                   This application allows users to monitor targeted file systems, like directory
                   folder, or single file in real-time. You can monitor and watch directories
                   added, new files created, deleted files, or modified files.
               """
        my_label = CTkLabel(top, text=about_message)
        my_label.pack()

    def exit(self):
        """Exits the application, and asks the user if they want to save the data."""
        if self.__saved is False:
            close = messagebox.askyesnocancel("Exit", "Do you want to save current data?")
            if close:
                file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                         filetypes=[("CSV files", "*.csv"),
                                                                    ("All files", "*.*")])

                if file_path:
                    with open(file_path, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerows('fe')
                    print(f"CSV file saved to: {file_path}")
                self.db_clear()
                root.destroy()

            if close is False:
                root.destroy()
        if self.__saved is True:
            close = messagebox.askyesno("Exit", "Are you sure?")
            if close:
                self.db_clear()
                root.destroy()



if __name__ == "__main__":

    root = CTk()
    view = Tkinter_GUI(root)  # Now create the Tkinter_GUI view
    model = DatabaseManager()
    controller = FileWatch(model, view)  # Initialize controller, passing model and None for view initially
    view.controller = controller
    view.model = model

    root.mainloop()