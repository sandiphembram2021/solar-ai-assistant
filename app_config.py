"""
Configuration for Hugging Face Spaces deployment
"""
import os

# Hugging Face Spaces specific settings
HF_SPACE = os.getenv("SPACE_ID") is not None
HF_TOKEN = os.getenv("HF_TOKEN")

# Override some settings for HF deployment
if HF_SPACE:
    # Use environment variables in HF Spaces
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # Disable some features that might not work in HF Spaces
    ENABLE_FILE_UPLOAD = True
    MAX_FILE_SIZE = 10  # MB
    
    print("Running in Hugging Face Spaces mode")
else:
    # Local development settings
    from dotenv import load_dotenv
    load_dotenv()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    ENABLE_FILE_UPLOAD = True
    MAX_FILE_SIZE = 10  # MB
