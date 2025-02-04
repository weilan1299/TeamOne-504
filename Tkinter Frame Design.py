import tkinter as tk
from tkinter import ttk
from tkinter import *

import customtkinter
from customtkinter import *
from customtkinter import CTkComboBox



customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

root = CTk()
root.title("File System Watcher")
root.geometry("800x600")

menubar = Menu(root)
root.config(menu=menubar)

#file menu
fileMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Start Watching")
fileMenu.add_command(label="Stop Watching")
fileMenu.add_command(label="Reset")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=quit)

#edit menu
editMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Browse for directory to watch")

#Database menu
dbMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Database", menu=dbMenu)
dbMenu.add_command(label="Write")
dbMenu.add_command(label="Clear database")
dbMenu.add_command(label="Delete database")
dbMenu.add_command(label="Change database")
dbMenu.add_separator()
dbMenu.add_command(label="Query")

#Help
HelpMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=HelpMenu)
HelpMenu.add_command(label="About")
HelpMenu.add_command(label="Usage Help")
HelpMenu.add_command(label="Shortcut Keys")





frame = Frame(root)
frame.pack(fill="both", expand=True)
#
# #creating the first frame
frame1 = Frame(frame, borderwidth=0, highlightthickness=10, relief="flat")
frame1.grid(row=0, column=0, padx=20, pady=20, sticky='w')
#
StW_button = CTkButton(master=frame1, text="Start Watching", corner_radius=20, width=10, cursor="hand2", border_color="#FFCC70", border_width=3)

StW_button.grid(row=0, column=0, sticky='w', padx=0, pady=0)

#
stop_button = CTkButton(frame1, text="Stop Watching", corner_radius=20, width=10, cursor="hand2",border_color="#FFCC70", border_width=3)
stop_button.grid(row=0, column=1, sticky='w', padx=0, pady=0)
#
reset = CTkButton(frame1, text="Reset", corner_radius=20, width=10, cursor="hand2", border_color="#FFCC70", border_width=3)
reset.grid(row=0, column=2)

for widget in frame1.winfo_children():
    widget.grid_configure(padx=5, pady=5)


# creating the second frame for path input
def openFile():
    filepath = filedialog.askdirectory()
    entry_var.set(filepath)




frame2 = Frame(frame, bd=5, relief="solid", borderwidth=0)
frame2.grid(row=1, column=0, sticky="news", padx=0, pady=0)



path_txt = Label(frame2, text="Directory to watch:")
entry_var = StringVar()
path_entry = CTkEntry(master=frame2, width=200, placeholder_text="Insert the path to directory", textvariable=entry_var)
path_txt.grid(row=0, column=0, sticky="w")
path_entry.grid(row=1, column=0, columnspan=8, sticky="w")


start_button = Button(frame2, text="Start",bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black")
stop_button = Button(frame2, text="Stop",bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black")
browse_button = Button(frame2, text="Browse",bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black",
                       command=openFile)

start_button.grid(row=2, column=0, sticky="w")
stop_button.grid(row=2, column=0)
browse_button.grid(row=2, column=2)


extension = Label(frame2, text="Extension:")
extension_combo = CTkComboBox(master=frame2, values=["", ".txt", ".py", ".exe"])
check_box = CTkCheckBox(master=frame2, text="Watch directories?")
extension.grid(row=0, column=9, sticky="w")
extension_combo.grid(row=1, column=9)
check_box.grid(row=2, column=9)

info_txt= Label(frame2, text="Leave blank for All files")
info_txt.grid(row=1, column=10, columnspan=2, sticky="w")



for widget in frame2.winfo_children():
    widget.grid_configure(padx=40, pady=5)

#creating the third frame
def database_path():
    file_path = filedialog.askdirectory()
    database_entry.set(file_path)


frame3 =Frame(frame, bd=5, relief="solid", borderwidth=0)
frame3.grid(row=2, column=0, sticky="news", padx=0, pady=0)

db_txt = Label(frame3, text="Database path:")
database_entry = StringVar()
db_entry = CTkEntry(frame3, width=200, placeholder_text="Database path", textvariable=database_entry)
db_txt.grid(row=0, column=0, sticky="w")
db_entry.grid(row=1, column=0,columnspan=8, sticky="w")

write_button =Button(frame3, text="Write", bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black")
clear_button =Button(frame3, text="Clear DB", bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black", width=6)
db_browse_button = Button(frame3, text="Browse", bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black",
                          command=database_path)
write_button.grid(row=2, column=0, sticky="w")
clear_button.grid(row=2, column=0,  sticky="e")
db_browse_button.grid(row=2, column=2)

db_extension = Label(frame3, text="Extension:")
extension_combo = CTkComboBox(master=frame3, values=["", "Option 1", "Option 2", "Option 3"])
db_extension.grid(row=0, column=9, sticky="w")
extension_combo.grid(row=1, column=9)

event_type = Label(frame3, text="Event Type:")
event_type_combo = CTkComboBox(master=frame3, values=["", "1", "2", "3"])
query_button = Button(frame3, text="Query", bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black")
event_type.grid(row=0, column=10, sticky="w")
event_type_combo.grid(row=1, column=10, sticky="w")
query_button.grid(row=2, column=10)

for widget in frame3.winfo_children():
    widget.grid_configure(padx=40, pady=5)

#forth frame

frame4 = CTkScrollableFrame(master=frame, orientation="vertical", border_color="#FFCC70", border_width=3)
frame4.grid(row=3, column=0, sticky="news", padx=20, pady=20)
txt_file = Label(frame4, text="File System Watcher Events:")
txt_file.grid(row=0, column=0, sticky="w")

file_name= Label(frame4, text="File Name")
file_name.grid(row=1, column=0, sticky="w", padx=40, pady=5)

path_event=Label(frame4, text="Path")
path_event.grid(row=1, column=1,columnspan=8 ,sticky="w", padx=0, pady=5)

event_frame4= Label(frame4, text="Event Type")
event_frame4.grid(row=1, column=9, columnspan=2,sticky="e", padx=100, pady=5)

time_stamp= Label(frame4, text="Time Stamp")
time_stamp.grid(row=1, column=12,columnspan=2,sticky="e", padx=0, pady=5)


root.mainloop()

