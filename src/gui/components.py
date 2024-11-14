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
        self.frame = customtkinter.CTkFrame(parent)
        
        self.label = customtkinter.CTkLabel(self.frame, text="Select Template:")
        self.var = customtkinter.StringVar()
        self.dropdown = customtkinter.CTkOptionMenu(
            self.frame,
            variable=self.var,
            values=templates,
            command=on_change
        )
        self.browse_button = customtkinter.CTkButton(
            self.frame,
            text="Change Template Directory",
            command=self.browse_directory
        )
        
        self.label.pack(pady=(5,0))
        self.dropdown.pack(pady=(0,5))
        self.browse_button.pack(pady=(0,5))
    
    def pack(self):
        self.frame.pack(fill='x', padx=5, pady=2)
    
    def get(self):
        return self.var.get()
    
    def set(self, value):
        self.var.set(value)
    
    def browse_directory(self):
        # This should be implemented in the main app class
        pass 