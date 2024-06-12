import pytest
from app import app as flask_app
from db import db
from setup_env import TestingConfig
from flask_migrate import upgrade

@pytest.fixture
def app():
    flask_app.config.from_object(TestingConfig)
    with flask_app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return flask_app.test_client()

# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()