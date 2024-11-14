import customtkinter
from tkinter import filedialog

class InputField:
    def __init__(self, parent, label_text, on_return=None):
        self.frame = customtkinter.CTkFrame(parent)
        
        # Create label with default color
        self.label = customtkinter.CTkLabel(
            self.frame,
            text=label_text,
            text_color="gray"
        )
        self.entry = customtkinter.CTkEntry(self.frame)
        
        self.label.pack(pady=(5,0))
        self.entry.pack(pady=(0,5))
        
        if on_return:
            self.entry.bind("<Return>", on_return)
    
    def set_status(self, is_valid):
        """Update label color based on validation"""
        color = "green" if is_valid else "red"
        self.label.configure(text_color=color)
    
    def pack(self):
        self.frame.pack(fill='x', padx=5, pady=2)
    
    def pack_forget(self):
        self.frame.pack_forget()
    
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
            text="Browse",
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