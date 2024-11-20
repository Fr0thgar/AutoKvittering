import json
import os
from utils.logger import Logger
import customtkinter

class ConfigManager:
    def __init__(self):
        self.logger = Logger()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(self.base_dir, 'config.json')
        self.theme_file = os.path.join(self.base_dir, 'resources/themes/theme.json')
        self.config = self.load_config()
        self.theme = self.load_theme()
        self.resolve_paths()
    
    def resolve_paths(self):
        """Convert relative paths to absolute paths"""
        # Resolve template directory
        if not os.path.isabs(self.config["template_directory"]):
            self.config["template_directory"] = os.path.join(
                self.base_dir,
                self.config["template_directory"]
            )

        # Create template directory if it doesn't exist
        if not os.path.exists(self.config["template_directory"]):
            os.makedirs(self.config["template_directory"])
            self.logger.info(f"Created template directory: {self.config['template_directory']}")
    
    def load_config(self):
        """Load configuration from a JSON file"""
        try:
            if not os.path.exists(self.config_file):
                return self.create_default_config()
            
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            self.logger.error("Configuration file is invalid or corrupted.")
            customtkinter.CTkMessageBox.show_error("Error", "Configuration file is invalid. Please check the file.")
            return self.create_default_config()  # Fallback to default config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            customtkinter.CTkMessageBox.show_error("Error", "Failed to load configuration. Please try again.")
            return self.create_default_config()  # Fallback to default config
    
    def load_theme(self):
        """Load theme from a JSON file"""
        try:
            if not os.path.exists(self.theme_file):
                return {}
            
            with open(self.theme_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            self.logger.error("Theme file is invalid or corrupted.")
            customtkinter.CTkMessageBox.show_error("Error", "Theme file is invalid. Please check the file.")
            return {}  # Fallback to default theme
        except Exception as e:
            self.logger.error(f"Error loading theme: {str(e)}")
            customtkinter.CTkMessageBox.show_error("Error", "Failed to load theme. Please try again.")
            return {}  # Fallback to default theme
    
    def create_default_config(self):
        """Create a default configuration"""
        default_config = {
            "template_directory": "",
            "theme_directory": "",
            "last_used_template": "",
            "last_used_theme": "",
            "output_directory": "",
            "button_fg_color": "lightblue",
            "button_hover_color": "blue",
            "button_text_color": "white"
        }
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config):
        """Save the configuration to a JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def create_default_config(self):
        """Create a default configuration and save it to a file"""
        default_config = {
            "template_directory": "resources/templates",
            "theme_directory": "resources/themes",
            "window_size": {
                "width": 500,
                "height": 400
            },
            "password_settings": {
                "length": 12,
                "use_uppercase": True,
                "use_lowercase": True,
                "use_digits": True,
                "use_special": True,
                "special_chars": "!@#$%^&*"
            }
        }
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config):
        """Save the configuration to a JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)  # Ensure the file object is passed correctly 