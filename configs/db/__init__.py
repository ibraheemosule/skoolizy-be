from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def drop_alembic_version():
    """Drops the alembic_version table"""
    db.session.execute(text('DROP TABLE IF EXISTS alembic_version'))
    db.session.commit()
    print('alembic_version table dropped.')
