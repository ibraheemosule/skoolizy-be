from flask_mysqldb import MySQL
from flask import Flask
from api.announcements.schema import announcements_schema
import os

def load_schemas(app: Flask, mysql: MySQL) -> None:
    for key, value in os.environ.items():
        print(f"{key}: {value}")
    with app.app_context():  # Ensure that we're in the application context
        conn = mysql.connection.cursor()
        conn.execute(announcements_schema)
        mysql.connection.commit()
        conn.close()
