import os
import pytest

from app import app
from app.models import db as _db


TEST_DB = 'test_project.db'
TEST_DB_PATH = "/opt/project/data/{}".format(TEST_DB)
TEST_DATABASE_URI = 'sqlite:///' + TEST_DB_PATH


@pytest.fixture(scope='session')
def app():
    """Session-wide test `Flask` application."""

    app.config.update(dict(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=TEST_DATABASE_URI,
    ))

    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TEST_DB_PATH):
        os.unlink(TEST_DB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TEST_DB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session