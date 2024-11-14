import customtkinter
from tkinter import filedialog

class InputField:
    def __init__(self, parent, label_text, on_return=None):
        self.label = customtkinter.CTkLabel(parent, text=label_text)
        self.entry = customtkinter.CTkEntry(parent)
        if on_return:
            self.entry.bind("<Return>", on_return)
    
    def pack(self):
        self.label.pack()
        self.entry.pack()
    
    def pack_forget(self):
        self.label.pack_forget()
        self.entry.pack_forget()
    
    def get(self):
        return self.entry.get()
    
    def set(self, value):
        self.entry.delete(0, 'end')
        self.entry.insert(0, value)

class TemplateSelector:
    def __init__(self, parent, templates, on_change=None):
        self.label = customtkinter.CTkLabel(parent, text="Select Template:")
        self.var = customtkinter.StringVar()
        self.dropdown = customtkinter.CTkOptionMenu(
            parent,
            variable=self.var,
            values=templates,
            command=on_change
        )
        self.browse_button = customtkinter.CTkButton(
            parent,
            text="Change Template Directory",
            command=self.browse_directory
        )
    
    def pack(self):
        self.label.pack()
        self.dropdown.pack()
        self.browse_button.pack(pady=10)
    
    def get(self):
        return self.var.get()
    
    def set(self, value):
        self.var.set(value)
    
    def browse_directory(self):
        # This should be implemented in the main app class
        pass 