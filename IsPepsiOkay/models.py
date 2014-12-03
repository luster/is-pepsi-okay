from flask.ext.login import UserMixin
import json
import locale
locale.setlocale(locale.LC_ALL, '')

class Tmp(object):

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

class DTmp(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

class User(UserMixin):

    def __init__(self, uid, username, email, password, dob, active=True):
        self.uid = uid
        self.username = username
        self.email = email
        self.password = password
        self.active = active
        self.dob = dob

    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.username)

class Movie(object):

    def __init__(self, mid, title, mdate, runtime, languages, description, budget, box_office, country):
        self.mid = mid
        self.title = title
        self.mdate = mdate
        self.runtime = runtime
        self.languages = languages.split(",")
        self.description = description
        self.budget = locale.currency(budget, grouping=True)[:-3] if budget else None
        self.box_office = locale.currency(box_office, grouping=True)[:-3] if box_office else None
        self.country = country.split(",")
        self.directors = list()
        self.writers = list()
        self.producers = list()
        self.actors = list()
        self.composers = list()
        self.genres = list()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


class Person(object):

    def __init__(self, pid, pname, pdob):
        self.pid = pid
        self.pname = pname
        self.pdob = pdob

    def get_credits(self):
        return database.get_credits_by_person(self.pid)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

class Credit(object):

    def __init__(self, pid, mid, d, p, w, c, a):
        self.pid = pid
        self.mid = mid
        self.directed = d
        self.produced = p
        self.wrote = w
        self.composed = c
        self.acted = a

class Genre(object):

    def __init__(self, gid, gname):
        self.gid = gid
        self.gname = gname

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

