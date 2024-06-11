import pytest
from app import app as flask_app
from setup_env import TestingConfig

@pytest.fixture
def app():
    flask_app.config.from_object(TestingConfig)
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()