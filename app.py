from flask import Flask
from flask_mysqldb import MySQL
from api.announcements.routes import announcements_bp
from api.schema_config import load_schemas
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'LIVERpool55.'
app.config['MYSQL_DB'] = 'skoolizy'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

app.register_blueprint(announcements_bp)

if __name__ == '__main__':
    load_schemas(app, mysql)
    app.run(debug=True, port=8080)
