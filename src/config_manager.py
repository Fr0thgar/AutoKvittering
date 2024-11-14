import json
import os
from utils.logger import Logger

class ConfigManager:
    def __init__(self):
        self.logger = Logger()
        self.config_file = 'config.json'
        self.config = self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    self.logger.error("Config file is corrupted")
                    return self.create_default_config()
        except FileNotFoundError:
            self.logger.warning("Config file not found, creating default")
            return self.create_default_config()
    
    def create_default_config(self):
        default_config = {
            "template_directory": os.path.join(os.getcwd(), "templates"),
            "window_size": {"width": 500, "height": 400},
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
        with open(self.config_file, 'w') as f:
            json.dump(config, indent=4)
        self.logger.info("Config saved successfully") 