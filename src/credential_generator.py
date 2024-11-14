import random
import string
from utils.logger import Logger

class CredentialGenerator:
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
    
    def generate_pin(self):
        pin = str(random.randint(100000, 999999))
        self.logger.info("Generated new PIN")
        return pin
    
    def get_print_pin(self, pin):
        return pin[-4:]
    
    def generate_password(self):
        settings = self.config["password_settings"]
        chars = ""
        required_chars = []
        
        if settings["use_lowercase"]:
            chars += string.ascii_lowercase
            required_chars.append(random.choice(string.ascii_lowercase))
            
        if settings["use_uppercase"]:
            chars += string.ascii_uppercase
            required_chars.append(random.choice(string.ascii_uppercase))
            
        if settings["use_digits"]:
            chars += string.digits
            required_chars.append(random.choice(string.digits))
            
        if settings["use_special"]:
            special = settings["special_chars"]
            chars += special
            required_chars.append(random.choice(special))
        
        remaining_length = settings["length"] - len(required_chars)
        password = required_chars + [random.choice(chars) for _ in range(remaining_length)]
        random.shuffle(password)
        
        self.logger.info("Generated new password")
        return ''.join(password) 