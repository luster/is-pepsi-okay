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
#
#ACTOR_QUERY = """INSERT INTO People (pname,pdob) VALUES """
## Code to generate Actor File Structure
#with open(DATA_DIR + '/uci/actors.html.better', 'r') as f:
#    count = 0
#    soup = BeautifulSoup(f.read())
#    tbl = soup.findAll('table')
#    for table in tbl:
#        for row in table.findAll('tr')[1:]:
#            cells = row.findAll('td')
#            if len(cells) > 0:
#                name = cells[0].contents[0][1:].replace('"','\"').replace("'",'\"').replace('`','\"')#.encode('ascii','replace')
#                ACTOR_QUERY += "('%s'" % (name)
#                dob = '0000-00-00'
#                if len(cells) > 5:
#                    dob = cells[5].contents[0][:]
#                    try:
#                        dob = int(dob)
#                        dob = "%d-01-01" % (dob)
#                    except:
#                        dob = '0000-00-00'
#                        #try:
#                        #    content = wikipedia.page(name).html()
#                        #    birth_year = int(re.match('.*born.*(\d{4})', content, re.DOTALL).group(1))
#                        #    print name + ' ' + str(birth_year)
#                        #    dob = '%d-01-01' % (birth_year)
#                        #except:
#                        #    pass
#
#                ACTOR_QUERY += ",'%s')," % (dob)
#                count += 1
#            if not count % 10:
#                print count
#    ACTOR_QUERY = ACTOR_QUERY[:-1] + ";"
#
#print 'Executing Actor Query...'
#cur.execute(ACTOR_QUERY)
#actors = cur.fetchall()
#
##########
#
#PEOPLE_QUERY = """INSERT INTO People (pname,pdob) VALUES """
#
#with open(DATA_DIR + '/uci/people.html', 'r') as f:
#    count = 0
#    soup = BeautifulSoup(f.read())
#    tbl = soup.findAll('table')
#    for table in tbl:
#        for row in table.findAll('tr')[1:]:
#            cells = row.findAll('td')
#            if len(cells) > 6:
#                #if 'A' not in ''.join(cells[1].contents):
#                if True:
#                    first_name = cells[5].contents[0][1:].replace('"','\"').replace("'",'\"').replace('`','\"')
#                    last_name = cells[4].contents[0][1:].replace('"','\"').replace("'",'\"').replace('`','\"')
#                    PEOPLE_QUERY += "('%s %s'" % (first_name, last_name)
#                    dob = '0000-00-00'
#                    dob = cells[6].contents[0][:]
#                    try:
#                        dob = int(dob)
#                        dob = "%d-01-01" % (dob)
#                    except:
#                        dob = '0000-00-00'
#
#                    PEOPLE_QUERY += ",'%s')," % (dob)
#                    count += 1
#                if not count % 10:
#                    print str(count)
#    PEOPLE_QUERY = PEOPLE_QUERY [:-1] + ";"
#
#print 'Executing People Query...'
#cur.execute(PEOPLE_QUERY)
#people = cur.fetchall()

####################
def wiki_parse(sidebar, header_text, multiple=0):
    try:
        strs = []
        elem = sidebar.find('th', text=header_text).parent.find('td')
        if not multiple:
            for s in elem.stripped_strings:
                # only return first one
                return s
        for s in elem.stripped_strings:
            strs.append(s)
        return strs
        #else:
        #    return elem.text.strip()
    except:
        if not multiple:
            return ''
        return []

def grab_col(tr, col_num):
    text = tr.xpath('./td[%d]//text()' % (col_num))
    if text:
        text = text[0].strip()
        return text
    return ''

def repr_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False
    except:
        return False

def closest_wiki_page(title, year):
    search = wikipedia.search(title)
    if search:
        if title in search[0] or 'film' in search[0]:
            return wikipedia.page(title)

def convert_to_int(s):
    cl = s.replace('$','').replace(',','')
    try:
        i = int(cl)
    except ValueError:
        pars = cl.split()
        i = int(float(pars[0]) * 1000000.)

    return i

def convert_runtime(r):
    if not r:
        return 0
    if 'minutes' in r:
        r = r.split()[0]
        return int(r)
    if 'hours' in r:
        r = r.split()[0]
        return int(float(r) * 60.)
    print r + '\tdafuq'
    return 0


from lxml import etree
movie_attrs = "mid,title,mdate,runtime,languages,description,budget,box_office,country"
MOVIE_QUERY = """INSERT INTO Movies (%s) VALUES """ % (movie_attrs)
with open(DATA_DIR + '/uci/main.html', 'r') as f:
    count = 0
    doc = etree.HTML(f.read())
    for tr in doc.xpath('//table/tr'):
        mid = grab_col(tr, 1)
        if not mid: continue

        title = grab_col(tr, 2)
        if not title or title[0:2] != "T:": continue
        title = title.split("T:")[1]

        rdate = grab_col(tr, 3)
        if not repr_int(rdate): continue
        releasedate = '%s-01-01' % (int(rdate))

        genre = grab_col(tr, 8)
        if not genre: continue

        if title != "Grease 2": continue

        page_name = "%s" % (title)
        try:
            wiki = wikipedia.page(page_name)
            summary = wiki.summary
            if 'film' not in summary and 'movie' not in summary and 'directed' not in summary:
                print 'here'
                wiki = wikipedia.page(page_name + ' (%s film)' %(rdate))
                summary = wiki.summary
                if rdate not in summary:
                    continue
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                wiki = wikipedia.page(page_name + ' (%s film)' %(rdate))
            except:
                continue
        except wikipedia.exceptions.PageError as e:
            continue

        if wiki and title.lower() in wiki.title.lower():
            count += 1
            print count
            print title
            # look for runtime, languages, *keywords, description
            # *tagline, budget, box_office, *mpaa rating, country
            wiki_soup = BeautifulSoup(wiki.html())

            sidebar = wiki_soup.find('table', {"class": 'infobox vevent'})

            description = wiki.summary.replace("'","''")

            runtime = wiki_parse(sidebar, 'Running time')
            runtime = convert_runtime(runtime)

            languages = ','.join(wiki_parse(sidebar, 'Language', True)).replace("'","''")
            country = ','.join(wiki_parse(sidebar, 'Country', True)).replace("'","''")

            budget = wiki_parse(sidebar, 'Budget')
            budget = convert_to_int(budget)

            box_office = wiki_parse(sidebar, 'Box office')
            box_office = convert_to_int(box_office)

            QUERY = MOVIE_QUERY + "('%s','%s','%s',%s,'%s','%s',%s,%s,'%s')" % (mid,
                    title,releasedate,runtime,languages,description,budget,box_office,country)
            print QUERY
            cur.execute(QUERY)
            result = cur.fetchall()
            print result
            break

            # involvement: direct, produce, write, music, act=0
            directed = wiki_parse(sidebar, 'Directed by', True)
            produced = wiki_parse(sidebar, 'Produced by', True)
            wrote = wiki_parse(sidebar, 'Written by', True)
            music = wiki_parse(sidebar, 'Music by', True)
            starred = wiki_parse(sidear, 'Starring', True)

            # set
            people = set().union(*[directed,produced,wrote,music,starred])
            while people:
                person = people.pop()
                #cur.execute('SELECT


            break
        break

cur.close()
db.commit()
db.close()

