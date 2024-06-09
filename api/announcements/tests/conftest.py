import pytest
from flask import Flask
from app import app
from api.schema_config import load_schemas
from setup_env import config

@pytest.fixture(scope='module')
def client():

    with app.app_context():  # Set up application context
        from app import mysql
        load_schemas(app, mysql)  # Ensure the test database is clean before tests

        with app.test_client() as client:
            yield client

@pytest.fixture(scope='function', autouse=True)
def clean_db():
    with app.app_context():  # Set up application context
        from app import mysql
        load_schemas(app, mysql)
