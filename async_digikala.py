import asyncio
from aiohttp import ClientSession
#import pathlib
import nest_asyncio
import lxml.html
#from unidecode import unidecode
import pandas as pd
import time
import json


# nest_asyncio.apply()
# subject='samsung cellphone'
# total_pages=10
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
async def fetch(url, session, page):
    async with session.get(url) as response:
        html_body = await response.text()
        return {"body": html_body, "page": page}

async def fetch_with_sem(sem, session, url, page):
    async with sem:
        return await fetch(url, session, page)

async def main(total,subject):
    tasks = []
    # semaphore
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for i in range(1, total+1):
            url = 'https://www.digikala.com/search/?has_selling_stock=1&q='+subject+'&pageno='+str(i)+'&sortby=21'
            #print("page", i, url)
            tasks.append(
                asyncio.create_task(
                    fetch_with_sem(sem, session, url, i)
                )
            )
        pages_content = await asyncio.gather(*tasks) 
        return pages_content


def output(total_pages,subject):
    t1=time.time()

    results = asyncio.run(main(total_pages,subject))
    t2=time.time()
    name=[]; link=[];price=[]; pic=[]; rate=[]; #send=[]; special=[]; exist=[]; 
    for result in results:
        html_data = result.get('body')
        tree=lxml.html.fromstring(html_data)
    
        for product in tree.xpath("//ul[@class='c-listing__items js-plp-products-list']/li"):
            name.append(product.xpath(".//div/@data-title-fa")[0])
            price.append(product.xpath(".//div/@data-price")[0])
            link.append('https://www.digikala.com'+product.xpath(".//a/@href")[0])
            pic.append(product.xpath(".//a/img/@src")[0])
            # send.append(product.xpath("normalize-space(//div[@class='c-product-box__status c-product-box__status--sbs']/text())")[0])
            # special.append(product.xpath("normalize-space(//div[@class='c-promotion__badge c-promotion__badge--special-sale ']/text())")[0])
            # exist.append(product.xpath("normalize-space(//div[@class='c-product-box__status']/text())")[0])
            rate.append(product.xpath("normalize-space(//div[@class='c-product-box__engagement-rating']/text())")[0])
            
    data={'name':name,'price':price,'link':link,'photo':pic, 'rate':rate}# 'send':send, 'special':special, 'exist':exist}
    
    df=pd.DataFrame(data=data)
    json_data=df.to_json(r'data.json',orient = 'records',force_ascii=False)
    # parsed = json.loads(json_data)
    # print(json.dumps(parsed, indent=4))
    writer=pd.ExcelWriter('data.xlsx')
    df.to_excel(writer,"Sheet1",index=False)
    writer.save()  
    t3=time.time()
    print(t2-t1,t3-t2)
    print(len(df))
    return(data)

#print(output(2,'قابلمه'))

