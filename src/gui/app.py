import tkinter as tk  # Import tkinter for menu functionality
import customtkinter
import os
import glob
from .components import InputField, TemplateSelector
from utils.logger import Logger
import json
from tkinter import filedialog  # Import filedialog for directory selection

class DocumentProcessorApp:
    def __init__(self, config_manager, document_processor, credential_generator):
        self.config = config_manager
        self.doc_processor = document_processor
        self.cred_generator = credential_generator
        self.logger = Logger()
        
        # Load theme before creating the window
        self.load_theme()
        
        self.root = customtkinter.CTk()
        self.setup_window()
        self.create_menu()
        self.create_widgets()
    
    def load_theme(self):
        """Load custom theme from JSON file"""
        try:
            theme_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "resources",
                "themes",
                "theme.json"
            )
            
            if os.path.exists(theme_path):
                with open(theme_path, 'r') as f:
                    theme = json.load(f)
                customtkinter.set_default_color_theme(theme_path)
                self.logger.info("Custom theme loaded successfully")
            else:
                self.logger.warning("Theme file not found, using default theme")
                
        except Exception as e:
            self.logger.error(f"Error loading theme: {str(e)}")
    
    def on_return(self, event=None):
        """Handle Enter key press"""
        self.process_document()
    
    def get_template_list(self):
        """Get list of template files from the configured directory"""
        try:
            template_dir = self.config.config["template_directory"]
            self.logger.info(f"Looking for templates in: {template_dir}")
            
            # Get full paths but only display filenames
            full_paths = glob.glob(os.path.join(template_dir, "*.docx"))
            
            # Return just the filenames
            template_names = [os.path.basename(path) for path in full_paths]
            
            if not template_names:
                self.logger.warning(f"No templates found in {template_dir}")
                return ["No templates found"]
                
            self.logger.info(f"Found templates: {template_names}")
            return template_names
            
        except Exception as e:
            self.logger.error(f"Error getting template list: {str(e)}")
            return ["Error loading templates"]
    
    def get_output_path(self, name):
        """Generate output path for the document"""
        from datetime import datetime
        current_year = datetime.now().strftime("%Y")
        current_month = datetime.now().strftime("%B")
        current_date = datetime.now().strftime("%d")
        
        output_dir = os.path.join(
            os.getcwd(),
            current_year,
            current_month,
            current_date
        )
        return os.path.join(output_dir, f"{name}.docx")
    
    def create_replacements_dict(self, name, username, pin, print_pin, password):
        """Create dictionary of replacements for the document"""
        return {
            "[Name]": name,
            "[NAME]": name.upper(),
            "[name]": name.lower(),
            "[Username]": username,
            "[USERNAME]": username.upper(),
            "[username]": username.lower(),
            "[Pin]": pin,
            "[PIN]": pin,
            "[pin]": pin,
            "[PrintPin]": print_pin,
            "[PRINTPIN]": print_pin,
            "[printpin]": print_pin,
            "[Password]": password,
            "[PASSWORD]": password,
            "[password]": password
        }
    
    def validate_inputs(self, template, name, username):
        """Validate user inputs"""
        if not template or template == "No templates found":
            self.logger.error("No template selected")
            return False
            
        if not name:
            self.logger.error("Name is required")
            return False
            
        if template != "Lagermedarbejder_skabelon.docx" and not username:
            self.logger.error("Username is required for this template")
            return False
            
        return True
    
    def show_result(self, success, message):
        """Show result to user"""
        if success:
            self.logger.info(message)
            # You could add a popup or status label here
        else:
            self.logger.error(message)
            # You could add an error popup here
    
    def setup_window(self):
        """Set up the main window properties"""
        self.root.title("Document Processor")
        self.root.geometry("600x400")  # Set a default size
        self.root.minsize(400, 300)  # Set a minimum size for the window

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=1)  # Template selector row
        self.root.grid_rowconfigure(1, weight=0)  # Status row
        self.root.grid_rowconfigure(2, weight=1)  # Input fields row
        self.root.grid_rowconfigure(3, weight=0)  # Button row
        self.root.grid_columnconfigure(0, weight=1)  # Main column
    
    def create_menu(self):
        """Create a menu bar with settings options"""
        menu_bar = tk.Menu(self.root)  # Use tkinter's Menu
        
        # Create a "Settings" menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Change Template Directory", command=self.change_template_directory)
        settings_menu.add_command(label="Change Theme Directory", command=self.change_theme_directory)
        settings_menu.add_separator()
        settings_menu.add_command(label="Exit", command=self.root.quit)
        
        # Add the settings menu to the menu bar
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        
        # Configure the menu bar
        self.root.config(menu=menu_bar)

    def change_template_directory(self):
        """Function to change the template directory"""
        new_directory = filedialog.askdirectory(title="Select Template Directory")  # Use tkinter's filedialog
        if new_directory:
            self.config.config["template_directory"] = new_directory
            self.config.save_config(self.config.config)  # Save the new config
            self.logger.info(f"Template directory changed to: {new_directory}")

    def change_theme_directory(self):
        """Function to change the theme directory"""
        new_directory = filedialog.askdirectory(title="Select Theme Directory")  # Use tkinter's filedialog
        if new_directory:
            self.config.config["theme_directory"] = new_directory
            self.config.save_config(self.config.config)  # Save the new config
            self.logger.info(f"Theme directory changed to: {new_directory}")

    def create_widgets(self):
        # Create main container frames
        self.top_frame = customtkinter.CTkFrame(self.root)
        self.status_frame = customtkinter.CTkFrame(self.root)
        self.input_frame = customtkinter.CTkFrame(self.root)
        self.button_frame = customtkinter.CTkFrame(self.root)
        
        # Pack frames into the grid
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.status_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.button_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Template selector in top frame
        self.template_selector = TemplateSelector(
            self.top_frame,
            self.get_template_list(),
            self.on_template_change
        )
        self.template_selector.pack(fill='x')  # Fill horizontally
        
        # Status label in status frame
        self.status_label = customtkinter.CTkLabel(
            self.status_frame,
            text="Please select a template",
            text_color="gray"
        )
        self.status_label.pack(pady=5)
        
        # Template info label
        self.template_info = customtkinter.CTkLabel(
            self.status_frame,
            text="",
            text_color="gray"
        )
        self.template_info.pack(pady=(0, 5))
        
        # Input fields in input frame
        self.name_input = InputField(
            self.input_frame,
            "Enter Name:",
            self.on_return
        )
        self.username_input = InputField(
            self.input_frame,
            "Enter Username:",
            self.on_return
        )
        
        # Submit button in button frame
        self.submit_button = customtkinter.CTkButton(
            self.button_frame,
            text="Submit",
            command=self.process_document
        )
        self.submit_button.pack(pady=10)
    
    def update_status(self, message, color="gray"):
        """Update status label with message and color"""
        self.status_label.configure(text=message, text_color=color)
    
    def update_template_info(self, template_name):
        """Update template info based on selected template"""
        if template_name == "Lagermedarbejder_skabelon.docx":
            info = "This template requires: Name only"
            self.template_info.configure(
                text=info,
                text_color="blue"
            )
        else:
            info = "This template requires: Name and Username"
            self.template_info.configure(
                text=info,
                text_color="blue"
            )
    
    def on_template_change(self, *args):
        """Handle template selection changes"""
        selected_template = self.template_selector.get()
        
        # First hide all input fields
        self.name_input.pack_forget()
        self.username_input.pack_forget()
        
        # Show appropriate fields based on the selected template
        if selected_template == "Lagermedarbejder_skabelon.docx":
            self.name_input.pack(pady=(5, 0))  # Show only the name input
            self.update_status("Lagermedarbejder template selected", "green")
        else:
            self.name_input.pack(pady=(5, 0))  # Show name input
            self.username_input.pack(pady=(5, 0))  # Show username input
            self.update_status("Brugeroplysninger template selected", "green")
        
        # Update template info
        self.update_template_info(selected_template)
    
    def process_document(self):
        """Process the document with the current inputs"""
        try:
            name = self.name_input.get()
            username = self.username_input.get()
            template = self.template_selector.get()
            
            if not self.validate_inputs(template, name, username):
                self.update_status("Please fill in all required fields", "red")
                return
            
            # Update status during processing
            self.update_status("Processing document...", "blue")
            self.root.update()  # Force GUI update
            
            # Generate credentials
            pin = self.cred_generator.generate_pin()
            print_pin = self.cred_generator.get_print_pin(pin)
            password = self.cred_generator.generate_password()
            
            # Create replacements and process document
            replacements = self.create_replacements_dict(
                name, username, pin, print_pin, password
            )
            
            template_path = os.path.join(
                self.config.config["template_directory"],
                template
            )
            
            success, message = self.doc_processor.process_document(
                template_path,
                self.get_output_path(name),
                replacements
            )
            
            if success:
                # Clear inputs first
                self.name_input.set("")
                self.username_input.set("")
                
                # Show success message with PIN
                success_message = f"Document created successfully!\nPIN: {pin}"
                self.update_status(success_message, "green")
                
                # Reset template info to default state
                self.update_template_info(template)
                
                # Force GUI update
                self.root.update()
            else:
                self.update_status(f"Error: {message}", "red")
            
        except Exception as e:
            self.logger.error(f"Error processing document: {str(e)}")
            self.update_status(f"Error: {str(e)}", "red")
    
    def run(self):
        self.root.mainloop() 