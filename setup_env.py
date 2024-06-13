import os
from dotenv import load_dotenv

load_dotenv()

class __Config:
    APP = os.getenv('FLASK_APP')
    PORT = int(os.getenv('FLASK_RUN_PORT'))
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 280}
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_DB_URI') +  os.getenv('FLASK_MYSQL_DB')
    DEBUG = False
    TESTING = False

class __DevelopmentConfig(__Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  os.getenv('FLASK_DB_URI') +  os.getenv('FLASK_MYSQL_DB_DEV')
class TestingConfig():
    SQLALCHEMY_DATABASE_URI =  'sqlite:///:memory:'
    TESTING = True

env = os.getenv('FLASK_ENV', 'development')
config = TestingConfig if env == 'testing' else __DevelopmentConfig if env == 'development' else __Config
__all__ = ['config', TestingConfig]

