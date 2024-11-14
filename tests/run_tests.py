import unittest
import sys
import os

# Add source directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test cases
from test_config_manager import TestConfigManager
from test_credential_generator import TestCredentialGenerator
from test_document_processor import TestDocumentProcessor

def run_tests():
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConfigManager))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCredentialGenerator))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDocumentProcessor))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 