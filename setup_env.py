import os
from dotenv import load_dotenv

load_dotenv()

class __Config:
    APP = os.getenv('FLASK_APP')
    PORT = int(os.getenv('FLASK_RUN_PORT'))
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_DB_URI') +  os.getenv('FLASK_MYSQL_DB')
    DEBUG = False
    TESTING = False

class __DevelopmentConfig(__Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  os.getenv('FLASK_DB_URI') +  os.getenv('FLASK_MYSQL_DB_DEV')

class TestingConfig():
    SQLALCHEMY_DATABASE_URI =  'sqlite:///:memory:'
    TESTING = True

config = __DevelopmentConfig if os.getenv('FLASK_ENV') == 'development' else __Config

__all__ = ['config', TestingConfig]

