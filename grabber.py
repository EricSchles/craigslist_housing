import lxml.html
import requests
import grequests
import pandas as pd

def minify(csv,price_range):
    df = pd.read_csv(csv)
    new_df = pd.DataFrame(columns=list(df.columns.values))
    for row in df:
        if df["price"] > price_range[1] and df["price"]<price_range[1]:
            

if __name__ == '__main__':
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
            try:
                dicter["time"] = html.xpath('//div[@class="content"]//span[@class="pl"]/time/@datetime')[ind]
            except:
                dicter["time"] = "no time given"
            try:
                dicter["title"] = [x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="pl"]/a')][ind]
            except:
                dicter["title"] = "no title given"
            try:
                dicter["price"] = int([x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="price"]')][ind].lstrip("$"))
            except:
                dicter["price"] = "no price given"
            try:
                dicter["housing"] =[x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="housing"]')][ind]
            except:
                dicter["housing"] = "no housing information given"
            try:
                dicter["area"] =[x.text_content().encode("ascii","ignore") for x in html.xpath('//div[@class="content"]//span[@class="l2"]/span[@class="pnr"]/small')][ind]
            except:
                dicter["area"] = "no area information given"
            try:
                dicter["link"] = ["http://newyork.craigslist.org"+x for x in html.xpath('//div[@class="content"]//span[@class="pl"]/a/@href')]
            except:
                dicter["link"] = "no link given"
            df = df.append(dicter,ignore_index=True)

    df.to_csv("results.csv")
