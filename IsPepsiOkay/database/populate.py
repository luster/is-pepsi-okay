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
    db=BaseConfig.MYSQL_DATABASE_DB,
    charset='utf8',
    use_unicode=True)

cur = db.cursor()

def free_mem():
    dont = ['os','MySQLdb','sys','re','wikipedia','BeautifulSoup',
            'PROJECT_DIR','DATA_DIR','BaseConfig','db','cur']

    a = []
    for var in globals():
        if "__" not in (var[:2],var[-2:]) and var not in dont:
            a.append(var)
    print a
    for var in a:
        del globals()[var]

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
del soup, tbl

print 'Executing Actor Query...'
cur.execute(ACTOR_QUERY)
db.commit()

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
del soup, tbl, f
print 'Executing People Query...'
cur.execute(PEOPLE_QUERY)
db.commit()

####################
def wiki_parse(sidebar, header_text, multiple=0):
    try:
        strs = []
        elem = sidebar.find('th', text=header_text).parent.find('td')
        if not multiple:
            for s in elem.stripped_strings:
                # only return first one
                return s.replace("'","''")
        for s in elem.stripped_strings:
            strs.append(s.replace("'","''"))
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
        text = text[0].strip().replace("'","''")
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
    if not s:
        return 0
    regex = re.compile(ur'[0-9\,]+',re.UNICODE)
    cl = s.replace('$','').replace(',','')
    try:
        i = int(cl)
    except ValueError:
        if 'million' in cl:
            pars = cl.split()
            try:
                i = int(float(pars[0]) * 1000000.)
                return i
            except ValueError:
                i = regex.search(cl)
                if i:
                    i = int(float(i.group(0)) * 1000000.)
                    return i
    i = regex.search(cl)
    if i:
        return i.group(0)
    return 0

def convert_runtime(r):
    if not r:
        return 0
    regex = re.compile('\d+', re.UNICODE)
    if 'minutes' in r:
        m = regex.search(r)
        if m:
            m = m.group(0)
        try:
            return int(m)
        except:
            print m + ' WTFFFFFFFFFF'
            return 0
    if 'hours' in r:
        m = regex.search(r)
        if m:
            m = m.group(0)
        try:
            return int(float(m) * 60.)
        except:
            print m + ' WTFFFFFFFFFFFFFFFFFF'
            return 0
    print r + '\tdafuq'
    return 0

#free_mem()
from lxml import etree
movie_attrs = "mid,title,mdate,runtime,languages,description,budget,box_office,country"
MOVIE_QUERY = """INSERT INTO Movies (%s) VALUES """ % (movie_attrs)

GENRE_QUERY = """INSERT INTO Genres (gname) VALUES """
PERSON_QUERY = """INSERT INTO People (pname) VALUES """
IS_GENRE_QUERY = """INSERT INTO Is_Genre (mid,gid) VALUES """

involved_attrs = "pid,mid,directed,produced,wrote,composed,acted"
INVOLVED_IN_QUERY = """INSERT INTO Involved_In (%s) VALUES """ % (involved_attrs)

def check_exists(cur, table, pkname, chkname, chkval):
    qry = """SELECT %s FROM %s WHERE %s='%s';""" % (pkname, table, chkname, chkval)
    print qry
    cur.execute(qry)
    r = cur.fetchone()
    print 'exists' + str(r)
    if not r:
        return False

    try:
        r = r[0]
        return r
    except TypeError:
        return r

print 'Starting Main Movie Data'
import gc
gc.collect()

#with open(DATA_DIR + '/uci/main.html', 'r') as f:
#    doc = etree.HTML(f.read())
#    for tr in doc.xpath('//table/tr'):
#        mid = grab_col(tr, 1)
#        print 'mid ' + mid
#        if not mid:
#            continue
#        if not check_exists(cur, 'Movies', 'mid', 'mid', mid):
#            continue
#        if check_exists(cur, 'Is_Genre', 'mid', 'mid', mid):
#            continue
#        genres = grab_col(tr, 8).split(',')
#        while genres:
#            genre = genres.pop().strip()
#            ggg = check_exists(cur, 'Genres', 'gid', 'gname', genre)
#            if ggg:
#                igq = IS_GENRE_QUERY + "('%s',%s);" % (mid, ggg)
#                print igq
#                cur.execute(igq)
#            else:
#                gq = GENRE_QUERY + "('%s');" % (genre)
#                print gq
#                cur.execute(gq)
#                gid = int(cur.lastrowid)
#                igq = IS_GENRE_QUERY + "('%s',%s);" % (mid,gid)
#                print igq
#                cur.execute(igq)




with open(DATA_DIR + '/uci/main.html', 'r') as f:
    count = 1
    doc = etree.HTML(f.read())
    tmpp = False
    for tr in doc.xpath('//table/tr'):
        mid = grab_col(tr, 1)
        #if mid == 'AMt10':
        #    tmpp = True
        #if not tmpp:
        #    print mid
        #    continue

        if not mid: continue
        #if check_exists(cur, 'Movies', 'mid', 'mid', mid):
        #    continue

        title = grab_col(tr, 2)
        title_orig = title.replace("''","'")
        if not title or title[0:2] != "T:": continue
        title = title.split("T:")[1]
        if not title: continue
        print '\n\n' + title

        # if title != "My Cousin Vinny": continue

        rdate = grab_col(tr, 3)
        if not repr_int(rdate): continue
        releasedate = '%s-01-01' % (int(rdate))

        genres = grab_col(tr, 8).split(',')
        print genres
        if not genres: continue
        if len(genres) == 1 and not genres[0]: continue
        gids = []
        while genres:
            genre = genres.pop().strip()
            ggg = check_exists(cur, 'Genres', 'gid', 'gname', genre)
            if not ggg:
                gq = GENRE_QUERY + "('%s');" % (genre)
                print gq
                cur.execute(gq)
                gids.append(int(cur.lastrowid))
            else:
                gids.append(ggg)
        db.commit()

        page_name = "%s" % (title_orig)
        try:
            wiki = wikipedia.page(page_name)
            summary = wiki.summary
            if 'film' not in summary and 'movie' not in summary and 'directed' not in summary:
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
            print str(count) + ' ' + title
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
            if not runtime and not languages and not country and not budget and not box_office:
                continue

            QUERY = MOVIE_QUERY + "('%s','%s','%s',%s,'%s','%s',%s,%s,'%s')" % (mid,
                    title,releasedate,runtime,languages,description,budget,box_office,country)
            print QUERY
            cur.execute(QUERY)
            db.commit()

            # genre & mid
            while gids:
                gid = gids.pop()
                mg_qry = IS_GENRE_QUERY + "('%s',%s)" % (mid,gid)
                print mg_qry
                cur.execute(mg_qry)
            db.commit()


            # involvement: direct, produce, write, music, act
            directed = wiki_parse(sidebar, 'Directed by', True)
            produced = wiki_parse(sidebar, 'Produced by', True)
            wrote = wiki_parse(sidebar, 'Written by', True)
            music = wiki_parse(sidebar, 'Music by', True)
            starred = wiki_parse(sidebar, 'Starring', True)

            # set
            people = set().union(*[directed,produced,wrote,music,starred])
            while people:
                person = people.pop()
                print person
                pid = check_exists(cur, 'People', 'pid', 'pname', person)
                print pid
                if not pid:
                    pq = PERSON_QUERY + "('%s')" % (person)
                    print pq
                    cur.execute(pq)
                    pid = cur.lastrowid
                pid = int(pid)
                db.commit()

                d = 1 if person in directed else 0
                p = 1 if person in produced else 0
                w = 1 if person in wrote else 0
                c = 1 if person in music else 0
                a = 1 if person in starred else 0

                ii_qry = INVOLVED_IN_QUERY + "(%s,'%s',%s,%s,%s,%s,%s);" % (pid,
                        mid,d,p,w,c,a)
                print ii_qry
                cur.execute(ii_qry)
                db.commit()


cur.close()
db.commit()
db.close()
