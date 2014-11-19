import wikipedia
from bs4 import BeautifulSoup as bs
import re

soup = bs(wikipedia.page('my cousin vinny 1992 film').html())
sidebar = soup.find('table', {"class": 'infobox vevent'})
