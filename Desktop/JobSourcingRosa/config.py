"""
Configuration settings for the Job Sourcing application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Google Sheets settings
    GOOGLE_SHEET_NAME = os.environ.get('GOOGLE_SHEET_NAME', 'EdJoin Education Jobs')
    SERVICE_ACCOUNT_FILE = os.environ.get('SERVICE_ACCOUNT_FILE', 'service_account.json')
    
    # Scraping settings
    MAX_PAGES_PER_ROLE = int(os.environ.get('MAX_PAGES_PER_ROLE', '10'))
    SCRAPING_DELAY = int(os.environ.get('SCRAPING_DELAY', '2'))
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    
    # Target roles for scraping
    TARGET_ROLES = [
        "director",
        "assistant director", 
        "dean",
        "principal",
        "superintendent"
    ]
