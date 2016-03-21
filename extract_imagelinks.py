#!/usr/bin/env python
# -*- coding: utf-8 -
import requests
from bs4 import BeautifulSoup

lines = open('page_links.txt', 'r').readlines()
for l in lines:
    l = l.strip()
    page = requests.get(l)
    html_doc = page.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    img = soup.find(class_='object-image')
    print img['data-src']
