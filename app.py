from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import Migrate
from sqlalchemy import text
from api.announcements.routes_announcements import announcements_bp
from api.staffs.routes_staffs import staffs_bp
from api.auth.routes_auth import auth_bp
from flask_cors import CORS
from configs import envs
from configs.app_configs import config
from configs.db import db
from utils.error_handlers import app_error_handlers
from api.account.routes_account import account_bp

app = Flask(__name__)

CORS(app)
app.config.from_object(config)


@app.cli.command('drop-alembic-version')
@with_appcontext
def drop_alembic_version():
    """Drops the alembic_version table"""
    db.session.execute(text('DROP TABLE IF EXISTS alembic_version'))
    db.session.commit()
    print('alembic_version table dropped.')


db.init_app(app)
migrate = Migrate(app, db)

app_error_handlers(app)
app.register_blueprint(announcements_bp)
app.register_blueprint(staffs_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)

if __name__ == "__main__":
    app.run(host=envs.FLASK_HOST, debug=envs.FLASK_DEBUG, port=envs.FLASK_PORT)
