from flask import Flask, request
from flask.cli import with_appcontext
from flask_migrate import Migrate
from api.announcements.routes_announcements import announcements_bp
from api.staffs.routes_staffs import staffs_bp
from api.auth.routes_auth import auth_bp
from flask_cors import CORS
from configs import envs
from configs.app_configs import config
from configs.db import db, drop_alembic_version
from utils.auth import decode_token, set_session_user
from utils.error_handlers import CustomError, app_error_handlers
from api.account.routes_account import account_bp

app = Flask(__name__)

CORS(app)
app.config.from_object(config)


@app.cli.command('drop-alembic-version')
@with_appcontext
def drop():
    drop_alembic_version()


db.init_app(app)
migrate = Migrate(app, db)


def auth_middleware(app):
    @app.before_request
    def authenticate_request():
        if request.method == "OPTIONS":
            # Skip authentication for preflight requests
            return

        open_routes = ['/login', '/signup']
        if request.path in open_routes:
            return

        if 'Authorization' not in request.headers:
            raise CustomError("Unauthorized", 401)

        token = request.headers['Authorization'].split(' ')

        if token[0] != 'Bearer' or len(token) < 2 or not token[1]:
            raise CustomError("Invalid token format provided", 401)

        request.session_user = decode_token(token=token[1])


set_session_user(app)
app_error_handlers(app)
app.register_blueprint(announcements_bp)
app.register_blueprint(staffs_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)

if __name__ == "__main__":
    app.run(host=envs.FLASK_HOST, debug=envs.FLASK_DEBUG, port=envs.FLASK_PORT)
