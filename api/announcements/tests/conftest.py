import pytest
from app import app as flask_app
from db import db


@pytest.fixture
def app():
    with flask_app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return flask_app.test_client()
