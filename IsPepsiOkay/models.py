from flask.ext.login import UserMixin

class User(UserMixin):

    def __init__(self, username, email, password, active=True):
        self.username = username
        self.email = email
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.username)

class Movie():
    pass

class Person():
    pass

class Genre():
    pass
