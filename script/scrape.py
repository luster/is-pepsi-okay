#!/usr/bin/env python

from lxml import html
import wikipedia

with open('movies.txt','r') as f:
    movies = f.read().strip().split('\n')

m = movies[0]

html = wikipedia.page(m).html()
tree = html.fromstring(html)

director = tree.xpath('//')
