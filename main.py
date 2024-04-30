from tkinter import *
import os
import shutil
import docx
import customtkinter
from datetime import *

customtkinter.set_default_color_theme("./theme.json")

def submit_name():
    name = name_entry.get()
    if name: 
        print("Name submitted: ", name)
    else:
        print("Please enter a name.")

    
# create the main app window
root = customtkinter.CTk()
root.title("Insert into Word")

# Create a label for the name input
name_label = customtkinter.CTkLabel(root, text="Enter Name: ")
name_label.pack()

# Create a text box for the name input
name_entry = customtkinter.CTkEntry(root)
name_entry.pack()

# Create a button to submit the name
submit_button = customtkinter.CTkButton(root, text="Submit", command=submit_name)
submit_button.pack()

root.mainloop()