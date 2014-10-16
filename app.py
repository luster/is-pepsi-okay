from flask import Flask
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ispepsiokay'
app.config['MYSQL_DATABASE_DB'] = 'IsPepsiOkay'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
    cursor = mysql.get_db().cursor()
    return "It's working, yayyy"

if __name__ == '__main__':
    app.run()
