from flask import Flask
from flask import request
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
    query = """SELECT uid,email,uname FROM Users"""
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()

    html = "<html><head></head><body>"
    html += "<table>"
    for u in users:
    	html += "<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (u[0],u[1],u[2])
    html += "</table></body></html>"
    return html

if __name__ == '__main__':
    app.run()
