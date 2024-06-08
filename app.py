from flask import Flask, request, jsonify, Response, json
from flask_mysqldb import MySQL
from typing import Dict, List
from api.announcements.routes import announcements_bp
from api.schema_config import load_schemas


app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'LIVERpool55.'
app.config['MYSQL_DB'] = 'skoolizy'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

app.register_blueprint(announcements_bp)


def create_announcements_table() -> None:
    with app.app_context():  # Ensure that we're in the application context
        conn = mysql.connection.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS announcements (
                        id INT NOT NULL AUTO_INCREMENT,
                        title VARCHAR(255) NOT NULL,
                        type ENUM('memo', 'single-day', 'multi-day') NOT NULL,
                        message VARCHAR(255) NOT NULL,
                        date DATE DEFAULT NULL,
                        time TIME DEFAULT NULL,
                        PRIMARY KEY (id),
                        CHECK ((type = 'memo' AND date IS NOT NULL) OR (type = 'single-day' AND time IS NOT NULL))
                       )''')
        mysql.connection.commit()
        conn.close()

# @app.route('/', methods=['GET'])
# def get_data() -> Response:
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM announcements")
#     data: List[Dict[str, int | str]] = cursor.fetchall()
#     res = json.dumps(data,  indent=1, sort_keys=True, default=str)
#     return json.loads(res)

# @app.route('/data', methods=['POST'])
# def insert_data() -> Response:
#     try:
#         data: Dict[str, str] = request.json
#         cursor = mysql.connection.cursor()
#         cursor.execute(
#             '''INSERT INTO announcements (title, type, message, date, time ) VALUES (%s, %s, %s, %s, %s)''', 
#             (data['title'], data['type'], data['message'], data['date'], data['time'])
#         )
#         mysql.connection.commit()
#         cursor.close()
#         return jsonify({'message': 'Data inserted successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    load_schemas(app, mysql)
    app.run(debug=True, port=8080)
