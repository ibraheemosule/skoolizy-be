import pytest
from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['MYSQL_DB'] = 'skoolizy_test'
    flask_app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()