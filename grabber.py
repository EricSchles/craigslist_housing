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
all_links = []
df = pd.DataFrame()
for r in responses:
    dicter = {}
    text = r.text.encode("ascii","ignore")
    html = lxml.html.fromstring(text)
    dicter["time"] = html.xpath('//div[@class="content"]/span[@class="pl"]/time/@datetime')
    dicter["title"] = html.xpath('//div[@class="content"]/span[@class="pl"]/a/')[0].text_content()
    dicter["price"] = html.xpath('//div[@class="content"]/span[@class="l2"]/span[@class="price"]')[0].text_content()
    dicter["housing"] = html.xpath('//div[@class="content"]/span[@class="l2"]/span[@class="housing"]')[0].text_content()
    dicter["area"] = html.xpath('//div[@class="content"]/span[@class="l2"]/span[@class="pnr"]/small')[0].text_content()
    
    df = df.append(dicter,ignore_index=True)

df.to_csv("results.csv")
