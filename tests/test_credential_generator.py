from test_base import TestBase
from src.credential_generator import CredentialGenerator
import re

class TestCredentialGenerator(TestBase):
    def setUp(self):
        super().setUp()
        self.generator = CredentialGenerator(self.test_config)

    def test_generate_pin(self):
        pin = self.generator.generate_pin()
        self.assertTrue(len(pin) == 6)
        self.assertTrue(pin.isdigit())

    def test_get_print_pin(self):
        pin = "123456"
        print_pin = self.generator.get_print_pin(pin)
        self.assertEqual(print_pin, "3456")

    def test_generate_password(self):
        password = self.generator.generate_password()
        
        # Test length
        self.assertEqual(len(password), 
                        self.test_config["password_settings"]["length"])
        
        # Test character types
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in self.test_config["password_settings"]["special_chars"] 
                         for c in password)
        
        self.assertTrue(has_upper)
        self.assertTrue(has_lower)
        self.assertTrue(has_digit)
        self.assertTrue(has_special) 