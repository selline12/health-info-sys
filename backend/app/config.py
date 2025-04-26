import os
from datetime import timedelta
import logging

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-please-change'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Redis configuration
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/health_info'
    
    # Fallback to SQLite if PostgreSQL is not available
    @classmethod
    def init_app(cls, app):
        try:
            # Test PostgreSQL connection
            from sqlalchemy import create_engine
            engine = create_engine(cls.SQLALCHEMY_DATABASE_URI)
            engine.connect()
        except Exception as e:
            app.logger.warning(f"PostgreSQL connection failed: {e}. Falling back to SQLite.")
            cls.SQLALCHEMY_DATABASE_URI = 'sqlite:///health_info.db'
        
        # Configure logging
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('logs/health_info.log',
                                         maxBytes=10240,
                                         backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Health Info System startup')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 