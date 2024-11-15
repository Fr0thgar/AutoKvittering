import customtkinter
from tkinter import filedialog

class InputField:
    def __init__(self, parent, label_text, on_return=None):
        self.frame = customtkinter.CTkFrame(parent)
        
        self.label = customtkinter.CTkLabel(self.frame, text=label_text)
        self.entry = customtkinter.CTkEntry(self.frame)
        
        self.label.pack(pady=(5, 0))
        self.entry.pack(pady=(0, 5))
        
        if on_return:
            self.entry.bind("<Return>", on_return)
    
    def pack(self, **kwargs):
        """Pack the frame with optional padding arguments"""
        self.frame.pack(fill='x', padx=5, pady=kwargs.get('pady', (0, 0)))
    
    def pack_forget(self):
        """Hide the input field"""
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
            text="Change Template Directory",
            command=self.browse_directory
        )
        
        self.label.pack(pady=(5,0))
        self.dropdown.pack(pady=(0,5))
        self.browse_button.pack(pady=(0,5))
    
    def pack(self, **kwargs):
        """Pack the frame with optional arguments"""
        self.frame.pack(padx=5, pady=2, **kwargs)
    
    def get(self):
        return self.var.get()
    
    def set(self, value):
        self.var.set(value)
    
    def browse_directory(self):
        # Implement directory browsing logic here
        pass