import wikipedia
from bs4 import BeautifulSoup as bs
import re

soup = bs(wikipedia.page('the sacrament 2013 film').html())
sidebar = soup.find('table', {"class": 'infobox vevent'})
cell = soup.find("th", text='Directed by').parent.find('td')
