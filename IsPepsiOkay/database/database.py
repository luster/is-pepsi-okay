from flask.ext.mysql import MySQL
from IsPepsiOkay.models import User, Movie, Person, Genre

class Database(object):

    def __init__(self, app):
        self.mysql = MySQL()
        self.mysql.init_app(app)
