import json
from tkinter import *
import os
import glob
import shutil
import docx
import customtkinter
from datetime import *

customtkinter.set_default_color_theme("./theme.json")

# function to load config with file paths
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # default config if file doesnt exist
        default_config = {
            "template_directory": os.path.join(os.getcwd(), "templates"),
            "window_size": {"width": 500, "height": 400}
        }
        # create config file with deafult values
        save_config(default_config)
        return default_config

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, indent=4)

def update_template_directory(new_path):
    config = load_config()
    config["template_directory"] = new_path
    save_config(config)

def browse_template_directory():
    from tkinter import filedialog
    config = load_config()
    new_dir = filedialog.askdirectory(initialdir=config["template_directory"])
    if new_dir:
        update_template_directory(new_dir)
        # Refresh template dropdown
        template_map = get_template_files()
        template_dropdown.configure(values=list(template_map.keys()))
        if template_map:
            template_var.set(list(template_map.keys())[0])

def get_template_files():
    config = load_config()
    template_dir = config["template_directory"]
    # Get full paths but only display filenames
    full_paths = glob.glob(os.path.join(template_dir, "*.docx"))
    # Create a dictionary mapping display names to full paths
    template_map = {os.path.basename(path): path for path in full_paths}
    return template_map

def submit_name(event=None):
    name = name_entry.get()
    selected_template_name = template_var.get()

    if name and selected_template_name: 
        # Get current month and date 
        current_month = datetime.now().strftime("%B")
        current_date = datetime.now().strftime("%d")
        current_year = datetime.now().strftime("%Y")
        folder_path = os.path.join(os.getcwd(), current_year, current_month, current_date)
        os.makedirs(folder_path, exist_ok=True)

        # Create folder paths
        file_path = os.path.join(folder_path, f"{name}.docx")

        # Load the template document
        template_path = template_map[selected_template_name]
        shutil.copyfile(template_path, file_path)

        doc = docx.Document(file_path)

        # Replace placeholder with submitted name 
        for paragraph in doc.paragraphs:
            if "[Name]" in paragraph.text:
                paragraph.text = paragraph.text.replace("[Name]", name)

        # Save the modified document
        output_path = os.path.join(folder_path, f"{name}.docx")
        doc.save(output_path)

        print("Document created: ", output_path)
    else:
        print("Please enter a name and select a template.")

    
# create the main app window
config = load_config()
root = customtkinter.CTk()
root.title("Insert into Word")
root.geometry(f"{config['window_size']['width']}x{config['window_size']['height']}")

# add template selection dropdown
template_label = customtkinter.CTkLabel(root, text="Select Template: ")
template_label.pack()

template_var = customtkinter.StringVar()
template_map = get_template_files()
template_dropdown = customtkinter.CTkOptionMenu(
    root,
    variable=template_var,
    values=list(template_map.keys())  # Only show filenames in dropdown
)
template_dropdown.pack()

settings_button = customtkinter.CTkButton(
    root,
    text="Change Template Directory",
    command=browse_template_directory
)
settings_button.pack(pady=10)

# If templates were found, set default value
if template_map:
    template_var.set(list(template_map.keys())[0])

# Create a label for the name input
name_label = customtkinter.CTkLabel(root, text="Enter Name: ")
name_label.pack()

# Create a text box for the name input
name_entry = customtkinter.CTkEntry(root)
name_entry.pack()

# Bind the Enter key to submit the name
name_entry.bind("<Return>", lambda event: submit_name())

# Create a button to submit the name
submit_button = customtkinter.CTkButton(root, text="Submit", command=submit_name)
submit_button.pack()

root.mainloop()