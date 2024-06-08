from flask import Flask
from flask_mysqldb import MySQL
from api.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
import os
from dotenv import load_dotenv

app = Flask(__name__)

env = os.getenv('ENV', 'development')

print(env)

if env == 'development':
    app.config.from_object(DevelopmentConfig)
elif env == 'testing':
    app.config.from_object(TestingConfig)
elif env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(Config)

mysql = MySQL(app)
