# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:36:25 2019

@author: Jan
"""

#html_doc = """
#<html><head><title>The Dormouse's story</title></head>
#<body>
#<p class="title"><b>The Dormouse's story</b></p>

#<p class="story">Once upon a time there were three little sisters; and their names were
#<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
#<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
#<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
#and they lived at the bottom of a well.</p>

#<p class="story">...</p>
#"""

from bs4 import BeautifulSoup
with open("sisters.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")
    



print(soup.title)
print(soup.title.name)
print(soup.title.string)