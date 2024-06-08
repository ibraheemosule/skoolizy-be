import pytest
from api import app
from api.setup_test_db import setup_test_db

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['ENV'] = 'testing'
    app.config['MYSQL_DB'] = 'test_sql'

    with app.test_client() as client:
        setup_test_db()  # Ensure the test database is clean before tests
        yield client

@pytest.fixture(scope='function', autouse=True)
def clean_db():
    setup_test_db()  # Reset the database before each test
