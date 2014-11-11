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
    
    data = []
    text = r.text.encode("ascii","ignore")
    html = lxml.html.fromstring(text)
    for ind in xrange(len(html.xpath('//div[@class="content"]//span[@class="pl"]/time'))):
        
        dicter = {}
        dicter["time"] = html.xpath('//div[@class="content"]//span[@class="pl"]/time')[ind]
        dicter["title"] = [x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="pl"]/a')][ind]
        dicter["price"] = [x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="price"]')][ind]
        dicter["housing"] =[x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="housing"]')][ind]

        dicter["area"] =[x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="pnr"]/small')][ind]
    
        
    
    df = df.append(dicter,ignore_index=True)

df.to_csv("results.csv")
