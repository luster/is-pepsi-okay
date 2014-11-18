#!/usr/bin/env python

import os
import MySQLdb
import sys
import re
import wikipedia
from bs4 import BeautifulSoup

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
        '..'))

DATA_DIR = os.path.abspath(
    os.path.join(PROJECT_DIR, '..', 'data'))

sys.path.insert(0, PROJECT_DIR)
from config import BaseConfig

db = MySQLdb.connect(
    host=BaseConfig.MYSQL_DATABASE_HOST,
    user=BaseConfig.MYSQL_DATABASE_USER,
    passwd=BaseConfig.MYSQL_DATABASE_PASSWORD,
    db=BaseConfig.MYSQL_DATABASE_DB)

cur = db.cursor()

cur.execute('DELETE FROM People;')
ra = cur.fetchall()

ACTOR_QUERY = """INSERT INTO People (pname,pdob) VALUES """
# Code to generate Actor File Structure
with open(DATA_DIR + '/uci/actors.html.better', 'r') as f:
    count = 0
    soup = BeautifulSoup(f.read())
    tbl = soup.findAll('table')
    for table in tbl:
        for row in table.findAll('tr')[1:]:
            cells = row.findAll('td')
            if len(cells) > 0:
                name = cells[0].contents[0][1:].replace('"','\"').replace("'",'\"').replace('`','\"')#.encode('ascii','replace')
                ACTOR_QUERY += "('%s'" % (name)
                dob = '0000-00-00'
                if len(cells) > 5:
                    dob = cells[5].contents[0][:]
                    try:
                        dob = int(dob)
                        dob = "%d-01-01" % (dob)
                    except:
                        dob = '0000-00-00'
                        #try:
                        #    content = wikipedia.page(name).html()
                        #    birth_year = int(re.match('.*born.*(\d{4})', content, re.DOTALL).group(1))
                        #    print name + ' ' + str(birth_year)
                        #    dob = '%d-01-01' % (birth_year)
                        #except:
                        #    pass

                ACTOR_QUERY += ",'%s')," % (dob)
                count += 1
            if not count % 10:
                print count
    ACTOR_QUERY = ACTOR_QUERY[:-1] + ";"

print 'Executing Actor Query...'
cur.execute(ACTOR_QUERY)
actors = cur.fetchall()

#########

PEOPLE_QUERY = """INSERT INTO People (pname,pdob) VALUES """

with open(DATA_DIR + '/uci/people.html', 'r') as f:
    count = 0
    soup = BeautifulSoup(f.read())
    tbl = soup.findAll('table')
    for table in tbl:
        for row in table.findAll('tr')[1:]:
            cells = row.findAll('td')
            if len(cells) > 6:
                #if 'A' not in ''.join(cells[1].contents):
                if True:
                    first_name = cells[5].contents[0][1:].replace('"','\"').replace("'",'\"').replace('`','\"')
                    last_name = cells[4].contents[0][1:].replace('"','\"').replace("'",'\"').replace('`','\"')
                    PEOPLE_QUERY += "('%s %s'" % (first_name, last_name)
                    dob = '0000-00-00'
                    dob = cells[6].contents[0][:]
                    try:
                        dob = int(dob)
                        dob = "%d-01-01" % (dob)
                    except:
                        dob = '0000-00-00'

                    PEOPLE_QUERY += ",'%s')," % (dob)
                    count += 1
                if not count % 10:
                    print str(count)
    PEOPLE_QUERY = PEOPLE_QUERY [:-1] + ";"

print 'Executing People Query...'
cur.execute(PEOPLE_QUERY)
people = cur.fetchall()

####################


MOVIE_QUERY = """INSERT INTO Movies (%s) VALUES """
with open(DATA_DIR + '/uci/main.html', 'r') as f:
    count = 0
    soup = BeautifulSoup(f.read())
    tbl = soup.findAll('table')
    for table in tbl:
        for row in table.findAll('tr')[1:]:
            cells = row.findAll('td')
            if len(cells) > 7:
                mid = cells[0].contents[0][1:]
                title = cells[1].contents[0][:].split("T:")[1]
                rdate = int(cells[2].contents[0][:])
                rdate = '%d-01-01' % (rdate)






cur.close()
db.commit()
db.close()

