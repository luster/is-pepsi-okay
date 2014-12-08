from flask.ext.mysql import MySQL
from flask import jsonify
from IsPepsiOkay.models import User, Movie, Person, Genre, Credit, DTmp
import json
from datetime import datetime

class Database(object):

    def __init__(self, app):
        self.mysql = MySQL()
        self.mysql.init_app(app)

    ####### USERS #######

    def get_all_users(self):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT uid, uname, email, pass FROM Users WHERE is_active = True"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        users = []
        for row in rows:
            users.append(User(row[0], row[1], row[2], row[3]))
        return users

    def get_user(self, username=None, email=None, password=None, dob=None):
        if email is None and username is None:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        first = True
        query = """SELECT uid, uname, email, pass, udob FROM Users WHERE """
        if username:
            query += """uname = '%s'""" % (username)
            first = False
        if email:
            if not first:
                query += """ AND """
            query += """email = '%s'""" % (email)
            first = False
        if password:
            if not first:
                query += """ AND """
            query += """pass = '%s'""" % (password)
        if dob:
            if not first:
                query += """ AND """
            query += """udob = '%s'""" % (dob)
        cursor.execute(query)
        u = cursor.fetchone()
        cursor.close()
        if not u:
            return None
        return User(u[1], u[2], u[3], u[4], u[0])

    def insert_user(self, username, email, password, dob):
        if (not (username and email and password)):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Users (uname, email, pass, udob) VALUES ('%s', '%s', '%s', '%s')""" % (username, email, password, dob)
        cursor.execute(statement)
        self.mysql.get_db().commit()
        cursor.close()
        return User(username, email, password, dob)

    def update_user(self, username, email=None, password=None, is_active=True):
        if (not (username) or not (email or password)):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """UPDATE Users SET is_active = %s""" % (str(is_active))
        if email:
            statement += """, email = '%s'""" % email
        if password:
            statement += """, pass = '%s'""" % password
        statement += """WHERE uname = '%s'""" % unsername
        cursor.execute(statement)
        self.mysql.get_db().commit()
        cursor.close()
        return User(username, email, password)

    ####### MOVIES #######

    def get_people_like(self, pname, limit=10):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT pid, pname FROM People WHERE pname LIKE '%s%%' OR pname LIKE '%%%s' OR pname LIKE '%%%s%%' LIMIT %s;""" % (pname, pname, pname, limit)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        r = []
        for result in results:
            r.append(dict(id=result[0],name=result[1]))
        return json.dumps(r)

    def get_movies_like(self, title, limit=5):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT mid, title FROM Movies WHERE title LIKE '%s%%' OR title LIKE '%%%s' OR title LIKE '%%%s%%' LIMIT %s;""" % (title, title, title, limit)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        r = []
        for result in results:
            r.append(dict(id=result[0],name=result[1]))
        return json.dumps(r)

    def get_genres_like(self, gname, limit=5):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT gid, gname FROM Genres WHERE gname LIKE '%s%%' OR gname LIKE '%%%s' OR gname LIKE '%%%s%%' LIMIT %s;""" % (gname, gname, gname, limit)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        r = []
        for result in results:
            r.append(dict(id=result[0],name=result[1]))
        return json.dumps(r)

    def get_movie_by_id(self, mid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        cols = "mid,title,mdate,runtime,languages,description,budget,box_office,country"
        query = """SELECT %s FROM Movies WHERE mid='%s';""" % (cols, mid)
        cursor.execute(query)
        movie = list(cursor.fetchone())
        cursor.close()
        r = {}
        lcols = cols.split(",")
        movie[2] = movie[2].year
        for (num,val) in enumerate(movie):
            r[lcols[num]] = val
        return Movie(*r)

    def get_movie_by_id(self, mid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        cols = "mid,title,mdate,runtime,languages,description,budget,box_office,country"
        #mids = ','.join(["'%s'" % (val) for val in mid])
        query = """SELECT %s FROM Movies WHERE mid='%s';""" % (cols, mid)
        cursor.execute(query)
        results = cursor.fetchone()
        cursor.close()
        if not results:
            return None
        movie = list(results)
        if movie[2]:
            movie[2] = movie[2].year
        return Movie(*movie)

    def get_people_from_movie(self, mid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        cols = "People.pid,pname,pdob"
        lcols = cols.split(",")
        query = """SELECT %s FROM Involved_In INNER JOIN People ON People.pid=Involved_In.pid WHERE mid='%s'""" % (cols, mid)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        results = [list(result) for result in results]
        people = []
        for person in results:
            if person[2]:
                person[2] = person[2].year
            else:
                person[2] = '0000'
            people.append(Person(*person))
        return people

    def get_all_credits_by_person(self, pid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        cols = "Movies.mid,Movies.title,directed,produced,wrote,composed,acted"
        lcols = cols.split(",")
        query = """SELECT %s FROM Involved_In INNER JOIN Movies ON Involved_In.mid=Movies.mid WHERE pid='%s'""" % (cols, pid)
        cursor.execute(query)
        results = list(cursor.fetchall())
        cursor.close()
        credits = []
        for credit in results:
            c = {}
            for (num,val) in enumerate(credit):
                c[lcols[num]] = val
                credits.append(c)
        return json.dumps(credits)

    def get_movie_credits_by_person(self, mid, pid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        cols = "pid,mid,directed,produced,wrote,composed,acted"
        lcols = cols.split(",")
        query = """SELECT %s FROM Involved_In WHERE pid='%s' AND mid='%s'""" % (cols, pid, mid)
        cursor.execute(query)
        results = list(cursor.fetchone())
        cursor.close()
        credit = Credit(*results)
        return credit

    def get_genre(self, mid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        cols = "gid,gname"
        query = """SELECT %s FROM Genres WHERE gid IN (SELECT gid FROM Is_Genre WHERE mid='%s');""" % (cols,mid)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        results = [list(result) for result in results]
        genres = [Genre(*x) for x in results]
        return genres

    def get_movies_by_genre(self, gid, limit=20):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT mid FROM Is_Genre WHERE gid=%s ORDER BY RAND() LIMIT %s;""" % (gid, limit)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        results = [result[0] for result in results]
        return results #mids

    def get_genre_name(self, gid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT gname FROM Genres WHERE gid=%s;""" % (gid)
        cursor.execute(query)
        results = cursor.fetchone()
        cursor.close()
        if not results:
            return None
        result = results[0]
        return result

    def get_person_name(self, pid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT pname FROM People WHERE pid=%s;""" % (pid)
        cursor.execute(query)
        results = cursor.fetchone()
        cursor.close()
        if not results:
            return None
        result = results[0]
        return result #pids

    def get_movies_by_person(self, pid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        cols = "Involved_In.mid,mdate,title,directed,produced,wrote,composed,acted"
        query = """SELECT %s FROM Involved_In JOIN Movies ON Involved_In.mid=Movies.mid WHERE pid=%s;""" % (cols,pid)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        lcols = cols.split(",")
        lcols[0] = "mid"
        if not results:
            return None
        results = [list(result) for result in results]
        for i in xrange(len(results)):
            if results[i][1]:
                results[i][1] = results[i][1].year
        movies = []
        for idx1,m in enumerate(results):
            tmp = {}
            for idx2,col in enumerate(lcols):
                tmp[col]=m[idx2]
            movies.append(DTmp(**tmp))
        return movies

    def rate(self, table, uid, pkey_name, oid, rating):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """INSERT INTO %s (uid,%s,urating) VALUES ('%s','%s','%s') ON DUPLICATE KEY UPDATE urating=VALUES(urating)""" % (table, pkey_name, uid, oid, rating)
        cursor.execute(query)
        results = cursor.fetchone()
        self.mysql.get_db().commit()
        cursor.close()
        if not results:
            return None
        results = list(results)
        return results

    def get_rating(self, table, uid, pkey_name, oid):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT urating FROM %s WHERE uid=%s AND %s='%s';""" % (table, uid, pkey_name, oid)
        cursor.execute(query)
        results = cursor.fetchone()
        cursor.close()
        if not results:
            return False, 0
        return True, results[0]

    def recommend(self, uid, limit=15):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """
            SELECT mid,title
            FROM Movies
            WHERE mid IN (
                SELECT DISTINCT(mid)
                FROM Movies
                WHERE mid IN (
                    SELECT mid
                    FROM Involved_In
                    WHERE pid IN (
                        SELECT pid
                        FROM Likes_Person
                        WHERE uid={0}
                        ORDER BY urating DESC
                    )
                )
                OR mid IN (
                    SELECT mid
                    FROM Involved_In
                    WHERE pid IN (
                        SELECT pid
                        FROM Involved_In
                        JOIN Has_Watched
                        ON Involved_In.mid=Has_Watched.mid
                        WHERE uid={0}
                        ORDER BY urating DESC
                    )
                )
            )
            AND mid NOT IN (
                SELECT mid
                FROM Has_Watched
                WHERE uid={0}
            )
            ORDER BY RAND()
            LIMIT {1};"""
        query = query.format(uid, limit)

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        results = [DTmp(**{'mid': r[0], 'title': r[1]}) for r in results]
        return results
