#!/usr/bin/env python

import os
import MySQLdb
import sys
import re
from bs4 import BeautifulSoup

def check_type(column_names):
    """
    column_names: (list of strings) MySQL column names)
    """

    t = {}

def build_query(filename, table_name, column_names, column_numbers,
    type_convert, offset=0):
    """
    filename: (string) absolute path to UCI data file
    table_name: (string) MySQL table name
    column_names: (list of strings) MySQL column names
    column_numbers: (list of integers) UCI column numbers
    type_convert: (list of types) type conversions if necessary

    """

    assert len(column_names) == len(column_numbers)


    cols = ",".join(column_names)
    QUERY = """INSERT INTO %s (%s) VALUES """ % (table_name, cols)

    # keep track of how many
    count = 0

    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read())
        tables = soup.findAll('table')
        for table in tables[offset:]:
            for row in table.findAll('tr')[1:]: # first row is header always
                cells = row.findAll('td')
                if len(cells) > 0:

