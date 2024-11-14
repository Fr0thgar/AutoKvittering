from config_manager import ConfigManager
from document_processor import DocumentProcessor
from credential_generator import CredentialGenerator
from gui.app import DocumentProcessorApp
from utils.logger import Logger

def main():
    logger = Logger()
    logger.info("Starting application")
    
    try:
        # Initialize components
        config_manager = ConfigManager()
        document_processor = DocumentProcessor(config_manager.config)
        credential_generator = CredentialGenerator(config_manager.config)
        
        # Create and run GUI
        app = DocumentProcessorApp(
            config_manager,
            document_processor,
            credential_generator
        )
        app.run()
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 