import lxml.html
import requests
import grequests
import pandas as pd
base_url = "http://newyork.craigslist.org/search/hhh"

pages = []
pages.append(base_url)
for i in xrange(1,20):
    pages.append(base_url+"?s="+str(i)+"00")
    
rs = (grequests.get(u) for u in pages)
responses = grequests.map(rs)
all_links = []
df = pd.DataFrame()
for r in responses:
    dicter = {}
    text = r.text.encode("ascii","ignore")
    html = lxml.html.fromstring(text)
    if html.xpath('//div[@class="content"]//span[@class="pl"]/time/@datetime') != []:
        dicter["time"] = html.xpath('//div[@class="content"]//span[@class="pl"]/time')
    else:
        dicter["time"] = ''
    if html.xpath('//div[@class="content"]//span[@class="pl"]/a') != []:
        dicter["title"] = [x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="pl"]/a')]
    else:
        dicter["title"] = ''
    if html.xpath('//div[@class="content"]/span[@class="l2"]//span[@class="price"]') != []:
        dicter["price"] = [x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="price"]')]
    else:
        dicter["price"] = ''
    if html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="housing"]') != []:
        dicter["housing"] = [x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="housing"]')]
    else:
        dicter["housing"] = ''
    if html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="pnr"]/small') != []:
        dicter["area"] = [x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="pnr"]/small')]
    else:
        dicter["area"] = ''
    df = df.append(dicter,ignore_index=True)

df.to_csv("results.csv")
