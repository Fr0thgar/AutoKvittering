from test_base import TestBase
from src.config_manager import ConfigManager
import os
import json

class TestConfigManager(TestBase):
    def test_load_valid_config(self):
        config_manager = ConfigManager()
        self.assertIsNotNone(config_manager.config)
        self.assertEqual(
            config_manager.config["window_size"]["width"],
            self.test_config["window_size"]["width"]
        )

    def test_load_invalid_config(self):
        # Write invalid JSON
        with open(self.test_config_path, 'w') as f:
            f.write("invalid json")
        
        config_manager = ConfigManager()
        self.assertIsNotNone(config_manager.config)
        self.assertTrue("window_size" in config_manager.config)

    def test_save_config(self):
        config_manager = ConfigManager()
        new_width = 600
        config_manager.config["window_size"]["width"] = new_width
        config_manager.save_config(config_manager.config)
        
        # Read config directly from file
        with open(self.test_config_path, 'r') as f:
            saved_config = json.load(f)
        
        self.assertEqual(saved_config["window_size"]["width"], new_width) 