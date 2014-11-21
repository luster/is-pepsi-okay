from flask.ext.mysql import MySQL
from IsPepsiOkay.models import User, Movie, Person, Genre

class Database(object):

    def __init__(self, app):
        self.mysql = MySQL()
        self.mysql.init_app(app)

    def get_all_users(self):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT username, email, password FROM Users WHERE is_active = True"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        users = []
        for row in rows:
            users.append(User(row[0], row[1], row[2]))
        return users

    def get_user(self, username=None, email=None, password=None):
        if email is None and username is None:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        first = True
        query = """SELECT username, email, password FROM Users WHERE"""
        if username:
            query += """username = '%s'""" % (username)
            first = False
        if email:
            if not first:
                query += """AND"""
            query += """email = '%s'""" % (email)
            first = False
        if password:
            if not first
                query += """AND"""
            query += """password = '%s'""" % (password)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        if not u:
            return None
        return User(u[0], u[1], u[2])

    def insert_user(self, username, email, password):
        if (not (username and email and password)):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Users (username, email, password) VALUES ('%s', '%s', '%s')""" % (username, email, password)
        cursor.execute(statement)
        self.mysql.get_db().commit()
        cursor.close()
        return User(username, email, password)

    def update_user(self, username, email=None, password=None, is_active=True):
        if (not (username) or not (email or password)):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """UPDATE Users SET is_active = %s""" % (str(is_active))
        if email:
            statement += """, email = '%s'""" % email
        if password:
            statement += """, password = '%s'""" % password
        statement = += """WHERE username = '%s'""" % unsername
        cursor.execute(statement)
        self.mysql.get_db().commit()
        cursor.close()
        return User(username, email, password)

