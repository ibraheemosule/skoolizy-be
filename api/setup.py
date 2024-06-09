import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    APP = os.getenv('FLASK_APP')
    PORT = os.getenv('FLASK_PORT')
    FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT')
    MYSQL_HOST = os.getenv('FLASK_MYSQL_HOST')
    MYSQL_PORT = os.getenv('FLASK_MYSQL_PORT')
    MYSQL_USER = os.getenv('FLASK_MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('FLASK_MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('FLASK_MYSQL_DB')
    MYSQL_CURSORCLASS = os.getenv('FLASK_MYSQL_CURSORCLASS')
    DEBUG = os.getenv('FLASK_DEBUG')
    TESTING = os.getenv('FLASK_TESTING')

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_DB = os.getenv('FLASK_MYSQL_DB_DEV')

class TestingConfig(Config):
    MYSQL_DB = os.getenv('FLASK_MYSQL_DB_TEST')
    TESTING = True

config = {
    'production': Config,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}[os.getenv('FLASK_ENV', 'development')]

__all__ = ['config']