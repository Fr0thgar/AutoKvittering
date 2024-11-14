import customtkinter
import os
import glob
from .components import InputField, TemplateSelector
from utils.logger import Logger

class DocumentProcessorApp:
    def __init__(self, config_manager, document_processor, credential_generator):
        self.config = config_manager
        self.doc_processor = document_processor
        self.cred_generator = credential_generator
        self.logger = Logger()
        
        self.root = customtkinter.CTk()
        self.setup_window()
        self.create_widgets()
    
    def get_template_list(self):
        """Get list of template files from the configured directory"""
        try:
            template_dir = self.config.config["template_directory"]
            # Get full paths but only display filenames
            full_paths = glob.glob(os.path.join(template_dir, "*.docx"))
            # Return just the filenames
            template_names = [os.path.basename(path) for path in full_paths]
            if not template_names:
                self.logger.warning("No templates found in directory")
                return ["No templates found"]
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
        window_size = self.config.config["window_size"]
        self.root.title("Document Processor")
        self.root.geometry(f"{window_size['width']}x{window_size['height']}")
    
    def create_widgets(self):
        # Template selector
        self.template_selector = TemplateSelector(
            self.root,
            self.get_template_list(),
            self.on_template_change
        )
        self.template_selector.pack()
        
        # Input fields
        self.name_input = InputField(
            self.root,
            "Enter Name:",
            self.on_return
        )
        self.name_input.pack()
        
        self.username_input = InputField(
            self.root,
            "Enter Username:",
            self.on_return
        )
        self.username_input.pack()
        
        # Spacing
        self.spacing = customtkinter.CTkLabel(self.root, text="")
        self.spacing.pack(pady=10)
        
        # Submit button
        self.submit_button = customtkinter.CTkButton(
            self.root,
            text="Submit",
            command=self.process_document
        )
        self.submit_button.pack(pady=10)
    
    def on_template_change(self, *args):
        template = self.template_selector.get()
        if template == "Lagermedarbejder_skabelon.docx":
            self.username_input.pack_forget()
        else:
            self.name_input.pack()
            self.username_input.pack()
        self.spacing.pack(pady=10)
        self.submit_button.pack(pady=10)
    
    def process_document(self):
        try:
            name = self.name_input.get()
            username = self.username_input.get()
            template = self.template_selector.get()
            
            if not self.validate_inputs(template, name, username):
                return
            
            # Generate credentials
            pin = self.cred_generator.generate_pin()
            print_pin = self.cred_generator.get_print_pin(pin)
            password = self.cred_generator.generate_password()
            
            # Create replacements dictionary
            replacements = self.create_replacements_dict(
                name, username, pin, print_pin, password
            )
            
            # Process document
            success, message = self.doc_processor.process_document(
                template,
                self.get_output_path(name),
                replacements
            )
            
            self.show_result(success, message)
            
        except Exception as e:
            self.logger.error(f"Error processing document: {str(e)}")
            self.show_result(False, str(e))
    
    def run(self):
        self.root.mainloop() 