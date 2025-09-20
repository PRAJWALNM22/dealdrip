"""
Production Configuration for Dealdrip Deployment
Handles environment variables and deployment settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///dealdrip.db')
    
    # Email Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    
    # WhatsApp Configuration - Twilio (Primary)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    
    # WhatsApp Configuration - Ultramsg (Secondary)
    ULTRAMSG_INSTANCE_ID = os.getenv('ULTRAMSG_INSTANCE_ID')
    ULTRAMSG_TOKEN = os.getenv('ULTRAMSG_TOKEN')
    
    # Scheduler Configuration
    PRICE_CHECK_HOUR = int(os.getenv('PRICE_CHECK_HOUR', 9))
    PRICE_CHECK_MINUTE = int(os.getenv('PRICE_CHECK_MINUTE', 0))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/dealdrip.log')
    
    # Deployment Platform Detection
    @staticmethod
    def get_platform():
        """Detect deployment platform"""
        if os.getenv('HEROKU_APP_NAME'):
            return 'heroku'
        elif os.getenv('RAILWAY_ENVIRONMENT'):
            return 'railway'  
        elif os.getenv('RENDER_EXTERNAL_URL'):
            return 'render'
        elif os.getenv('VERCEL_URL'):
            return 'vercel'
        elif os.getenv('NETLIFY'):
            return 'netlify'
        else:
            return 'local'

class ProductionConfig(Config):
    """Production specific configuration"""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    
    # Use stronger secret key in production
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

class DevelopmentConfig(Config):
    """Development specific configuration"""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing specific configuration"""
    FLASK_ENV = 'testing'
    DEBUG = False
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'  # In-memory database for tests

# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)

# For easy import
current_config = get_config()