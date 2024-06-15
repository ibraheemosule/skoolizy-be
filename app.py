import os
from flask import Flask
from flask_migrate import Migrate
from api.announcements.routes import announcements_bp
from flask_cors import CORS
from setup_env import config
from db import db

app = Flask(__name__)

CORS(app)
app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(announcements_bp)

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False), port=app.config.get("PORT", 5000))
