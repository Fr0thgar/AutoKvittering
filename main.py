from tkinter import *
import os
import shutil
import docx
import customtkinter
from datetime import *

customtkinter.set_default_color_theme("./theme.json")

def submit_name(event=None):
    name = name_entry.get()
    if name: 
        # Get current month and date 
        current_month = datetime.now().strftime("%B")
        current_date = datetime.now().strftime("%d")
        current_year = datetime.now().strftime("%Y")
        folder_path = os.path.join(os.getcwd(), current_year, current_month, current_date)
        os.makedirs(folder_path, exist_ok=True)

        # Create folder paths
        file_path = os.path.join(folder_path, f"{name}.docx")

        # Load the template document
        template_path = r"C:\Users\jbs\Code\AutoKvittering\Template.docx"
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
        print("Please enter a name.")

    
# create the main app window
root = customtkinter.CTk()
root.title("Insert into Word")
root.geometry("250x150")

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