from flask_mysqldb import MySQL
from api import app

def setup_test_db():
    app.config['MYSQL_DB'] = 'skoolizy_test'
    mysql = MySQL(app)
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS announcements")
        cursor.execute('''CREATE TABLE announcements (
                          id INT NOT NULL AUTO_INCREMENT,
                          title VARCHAR(255) NOT NULL,
                          type ENUM('memo', 'single-day', 'multi-day') NOT NULL,
                          message VARCHAR(255) NOT NULL,
                          date DATE DEFAULT NULL,
                          time TIME DEFAULT NULL,
                          PRIMARY KEY (id),
                          CHECK ((type = 'memo' AND date IS NOT NULL) OR (type != 'single-day' AND time IS NOT NULL))
                        )''')
        mysql.connection.commit()
        cursor.close()
