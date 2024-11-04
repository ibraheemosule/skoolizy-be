from configs import envs


class __Config:
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 280}
    SQLALCHEMY_DATABASE_URI = envs.MYSQL_DB_URI + envs.MYSQL_DB
    MYSQL_CURSORCLASS = envs.MYSQL_CURSORCLASS
    DEBUG = envs.FLASK_DEBUG
    TESTING = False


class __DevelopmentConfig(__Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = envs.MYSQL_DB_URI + (envs.MYSQL_DB_DEV or '')


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = envs.MYSQL_DB_URI_TEST
    TESTING = True


__env = envs.FLASK_ENV

selected_config = __Config

if __env == "testing":
    selected_config = TestingConfig
if __env == "development":
    selected_config = __DevelopmentConfig

config = selected_config

__all__ = ["config", TestingConfig]
