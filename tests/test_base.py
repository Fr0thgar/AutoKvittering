import unittest
import os
import shutil
import json

class TestBase(unittest.TestCase):
    def setUp(self):
        # Create test directory structure
        self.test_dir = "test_data"
        self.test_templates_dir = os.path.join(self.test_dir, "templates")
        self.test_output_dir = os.path.join(self.test_dir, "output")
        self.test_config_path = os.path.join(self.test_dir, "config.json")
        
        # Create directories
        os.makedirs(self.test_templates_dir, exist_ok=True)
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Create test config
        self.test_config = {
            "template_directory": self.test_templates_dir,
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
        
        with open(self.test_config_path, 'w') as f:
            json.dump(self.test_config, f)

    def tearDown(self):
        # Clean up test directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir) 