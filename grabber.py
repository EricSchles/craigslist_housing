import lxml.html
import requests
import grequests

base_url = "http://newyork.craigslist.org/search/hhh"

pages = []
pages.append(base_url)
for i in xrange(1,20):
    pages.append(base_url+"?s="+str(i)+"00")
    
rs = (grequests.get(u) for u in pages)
responses = grequests.map(rs)
for r in responses:
    