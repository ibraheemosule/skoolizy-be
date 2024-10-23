import os
from dotenv import load_dotenv

load_dotenv()


class __Config:
    APP = os.getenv("FLASK_APP")
    PORT = int(os.getenv("FLASK_RUN_PORT"))
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 280}
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_DB_URI") + os.getenv("MYSQL_DB")
    ACCESS_TOKEN_EXPIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")
    REFRESH_TOKEN_EXPIRES_DAYS = os.getenv('REFRESH_TOKEN_EXPIRES_DAYS')
    OTP_EXPIRY_TIME_IN_MINUTES = os.getenv('OTP_EXPIRY_TIME_IN_MINUTES')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MYSQL_CURSORCLASS = os.getenv('MYSQL_CURSORCLASS')
    DEBUG = False
    TESTING = False


class __DevelopmentConfig(__Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_DB_URI") + os.getenv("MYSQL_DB_DEV")


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True


env = os.getenv("FLASK_ENV", "development")
selected_config = __Config

if env == "testing":
    selected_config = TestingConfig
if env == "development":
    selected_config = __DevelopmentConfig

config = selected_config

__all__ = ["config", TestingConfig]
