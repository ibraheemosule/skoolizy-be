from flask_mysqldb import MySQL
from flask import Flask
from api.announcements.models import announcements_schema
import os

def load_schemas(app: Flask, mysql: MySQL) -> None:
    with app.app_context():
        conn = mysql.connection.cursor()
        conn.execute(announcements_schema)
        mysql.connection.commit()
        conn.close()
