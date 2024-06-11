import os
from dotenv import load_dotenv

load_dotenv()
class __Config:
    APP = os.getenv('FLASK_APP')
    PORT = int(os.getenv('FLASK_RUN_PORT'))
    MYSQL_HOST = os.getenv('FLASK_MYSQL_HOST')
    MYSQL_PORT = int(os.getenv('FLASK_MYSQL_PORT'))
    MYSQL_USER = os.getenv('FLASK_MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('FLASK_MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('FLASK_MYSQL_DB')
    MYSQL_CURSORCLASS = os.getenv('FLASK_MYSQL_CURSORCLASS')
    DEBUG = os.getenv('FLASK_DEBUG')
    TESTING = os.getenv('FLASK_TESTING')

class __DevelopmentConfig(__Config):
    DEBUG = True
    MYSQL_DB = os.getenv('FLASK_MYSQL_DB_DEV')

class TestingConfig(__Config):
    MYSQL_DB = os.getenv('FLASK_MYSQL_DB_TEST')
    TESTING = True

config = __DevelopmentConfig if os.getenv('FLASK_ENV') == 'development' else __Config

__all__ = ['config', TestingConfig]