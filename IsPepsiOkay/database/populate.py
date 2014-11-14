#!/usr/bin/env python

import os
import MySQLdb
import sys
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

ACTOR_QUERY = """INSERT INTO People (pname,pdob) VALUES """
# Code to generate Actor File Structure
with open(DATA_DIR + '/uci/actors.html.better', 'r') as f:
    num = 0
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
                    dob = row.findAll('td')[5].contents[0][:]
                    try:
                        dob = int(dob)
                        dob = "%d-01-01" % (dob)
                    except:
                        dob = '0000-00-00'
                ACTOR_QUERY += ",'%s')," % (dob)
                count += 1
            if not count % 50:
                print count
    ACTOR_QUERY = ACTOR_QUERY[:-1] + ";"

print 'Executing Query...'
cur.execute(ACTOR_QUERY)

print cur.rowcount
cur.close()
db.commit()
db.close()

print 'Works'
print num
