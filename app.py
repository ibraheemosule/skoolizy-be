from flask import Flask
from flask_migrate import Migrate
from api.announcements.routes import announcements_bp
from api.teachers.routes import teachers_bp
from api.auth.routes import auth_bp
from flask_cors import CORS
from setup_env import config
from db import db
from utils.error_handlers import app_error_handlers

app = Flask(__name__)

CORS(app)
app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)

app_error_handlers(app)
app.register_blueprint(announcements_bp)
app.register_blueprint(teachers_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False), port=app.config.get("PORT", 5000))
