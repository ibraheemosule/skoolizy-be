from flask import Flask
from flask_mysqldb import MySQL
from api.announcements.routes import announcements_bp
from api.schema_config import load_schemas
from flask_cors import CORS
from setup_env import config

app = Flask(__name__)

CORS(app)
app.config.from_object(config)

mysql = MySQL(app)
load_schemas(app, mysql)
app.register_blueprint(announcements_bp)

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', False), port=app.config.get('PORT', 5000))
