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

# Code to generate Actor File Structure
with open(DATA_DIR + '/uci/actors.html.better', 'r') as f:
    num = 0
    soup = BeautifulSoup(f.read())
    tbl = soup.findAll('table')
    for table in tbl:
        for row in table.findAll('tr')[1:]:
            if len(row.findAll('td')) > 0:
                num += 1
                print row.findAll('td')[0].contents[0][1:]

print 'Works'
print num
