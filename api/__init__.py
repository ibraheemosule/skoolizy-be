from flask import Flask
from flask_mysqldb import MySQL
from api.setup import Config, DevelopmentConfig, TestingConfig
import os
from dotenv import load_dotenv

app = Flask(__name__)

env = os.getenv('ENV', 'development')

print(env)

if env == 'development':
    app.config.from_object(DevelopmentConfig)
elif env == 'testing':
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(Config)

mysql = MySQL(app)
